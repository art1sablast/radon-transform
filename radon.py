from tkFileDialog import askopenfilename #gui

from scipy import misc #imread


imagename = askopenfilename() #gui
image = misc.imread(imagename, flatten=True).astype('float64')

if len(image.shape)==3: #returns three if the picture is color, else two
    image=grey_scale(image)

def grey_scale(photo): #greyscaling picture if it was color
    return photo[:,:,0]*0.299+photo[:,:,1]*0.587+photo[:,:,2]*0.114


