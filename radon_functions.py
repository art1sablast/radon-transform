from skimage import transform
from scipy import misc
from scipy.fftpack import fft, ifft, fftfreq
from scipy.interpolate import interp1d

import imageio 
import matplotlib as plt
import numpy as np
import helper_functions as help

def radon_skimage(image, theta):
    theta = None
    return transform.radon(image, None, True)

def iradon_skimage(sinogram):
    return transform.iradon(sinogram, theta=None, output_size=None, filter='ramp', interpolation='linear', circle=True)


def radon_transform(image, steps):
    sinogram = np.zeros((steps, len(image)), dtype='float64')
    for s in range(steps):
        rotation = misc.imrotate(image, -s*180/steps).astype('float64')
        sinogram[:,s] = sum(rotation)
    return sinogram


def iradon_transform(sinogram, theta=None, interpolation='linear'): #filtered back projection will kill me
    output_size = sinogram.shape[0]
    sinogram = help.sinogram_circle_to_square(sinogram) #stretching
    th = (np.pi / 180.0)*theta

    projection_size = \
        max(64, int(2**np.ceil(np.log2(2*sinogram.shape[0]))))
    size_width = ((0, projection_size - sinogram.shape[0]),(0,0))
    image = np.pad(sinogram, size_width, mode='constant', constant_values=0)

    f = fftfreq(projection_size).reshape(-1,1) #digital freq
    omega = 2 * np.pi * f                      #angular freq

    fourier_filter = 2 * np.abs(f) #Ram-Lak filter
    projection = fft(image, axis=0)*fourier_filter

    radon_filtered = np.real(ifft(projection, axis=0))
    radon_filtered = radon_filtered[:sinogram.shape[0],:]
    reconstructed = np.zeros((output_size, output_size))
    
    #backprojecting
    mid_index = sinogram.shape[0] // 2
    [X, Y] = np.mgrid[0:output_size, 0:output_size]
    xpr = X - int(output_size) // 2
    ypr = Y - int(output_size) // 2
    
    #interpolation
    ip_types = ('linear','nearest', 'cubic')
    if interpolation not in ip_types:
        raise ValueError("wrong interpolaion type")

    #print(len(theta))

    for i in range(len(theta)):
        t = ypr * np.cos(th[i]) - xpr * np.sin(th[i])
        x = np.arange(radon_filtered.shape[0])-mid_index
        if interpolation == 'linear':
            backprojected = np.interp(t, x, radon_filtered[:, i], left=0, right=0)
        else:
            interpolant = interp1d(x, radon_filtered[:, i], kind=interpolation, bounds_error=False, fill_value=0)
            backprojected = interpolant(t)
        reconstructed += backprojected

     #ronda szurkeseget kiszedni
    radius = output_size // 2
    cirrcle = (xpr ** 2 + ypr ** 2) <= radius ** 2
    reconstructed[~cirrcle] = 0.  

    return reconstructed * np.pi / (2*180)

