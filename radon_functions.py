from skimage import transform
from scipy import misc
import numpy as np

def radon_skimage(image, theta):
    return transform.radon(image, None, True)

#def iradon_skimage()


def radon_lili(image, steps):
    radon = np.zeros((steps, len(image)), dtype='float64')
    for s in range(steps):
        rotation = misc.imrotate(image, -s*180/steps).astype('float64')
        radon[:,s] = sum(rotation)
    return radon


#def iradon_lili()
