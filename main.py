import imageio
from skimage import transform
 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import gui_functions as gui
import helper_functions as help
import radon_functions as radon

image = imageio.imread(gui.imagename).astype('float64')

if len(image.shape) == 3: #returns three if the picture is color, else two
    image = help.grey_scale(image)

image = transform.resize(image,(180,180))
imageio.imwrite('greyscale.jpg', image)

sinogram_skimage = radon.radon_skimage(image, 180)
sinogram_lili = radon.radon_transform(image, 180)

#well we want to see how that worked so far
imageio.imwrite('sinogram_skimage.jpg', sinogram_skimage)
imageio.imwrite('sinogram_lili.jpg', sinogram_lili)

#this is where the fun, ehm i mean the reconstruction begins
#names start with rc_(reconstruction method)_from_(radon method) 
#rc stands for ReConstruction \o/

#reconstruction with skimage's built-in invert radon function
rc_skimage_from_skimage = radon.iradon_skimage(sinogram_skimage)
rc_skimage_from_lili = radon.iradon_skimage(sinogram_lili)
#let's see what we got
#rc - reconstructed, from skimage/lili radon and skimage/lili iradon
imageio.imwrite('skinverted_skiradon.jpg', rc_skimage_from_skimage)
imageio.imwrite('skinverted_liliradon.jpg', rc_skimage_from_lili)

#filtered back projection

theta = np.linspace(0, 180, max(image.shape), endpoint=False)

rc_lili_from_skimage = radon.iradon_transform(sinogram_skimage, theta=theta, interpolation='cubic')
rc_lili_from_lili = radon.iradon_transform(sinogram_lili, theta=theta, interpolation='cubic')
imageio.imwrite('lilinverted_skiradon.jpg', rc_lili_from_skimage)
imageio.imwrite('lilinverted_liliradon.jpg', rc_lili_from_lili)




