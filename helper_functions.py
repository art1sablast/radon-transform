import numpy as np

def grey_scale(photo): #greyscaling picture if it was color
    return photo[:,:,0]*0.299+photo[:,:,1]*0.587+photo[:,:,2]*0.114
    # L = R * 299/1000 + G * 587/1000 + B * 114/1000

def sinogram_circle_to_square(sinogram):
    diagonal = int(np.ceil(np.sqrt(2) * sinogram.shape[0]))
    pad = diagonal - sinogram.shape[0]
    old_center = sinogram.shape[0] // 2
    new_center = diagonal // 2
    #np.pad pads an array, 
    pad_before = new_center - old_center
    pad_width = ((pad_before, pad - pad_before), (0, 0))
    return np.pad(sinogram, pad_width, mode='constant', constant_values=0)
