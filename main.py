import imageio #imread
from skimage import transform
 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import gui_functions as gui
import helper_functions as help
import radon_functions as radon

image = imageio.imread(gui.imagename).astype('float64')

if len(image.shape)==3: #returns three if the picture is color, else two
    image=help.grey_scale(image)

image = transform.resize(image,(220,220))

imageio.imwrite('catcat.jpg', image)

