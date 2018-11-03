def grey_scale(photo): #greyscaling picture if it was color
    return photo[:,:,0]*0.299+photo[:,:,1]*0.587+photo[:,:,2]*0.114
    # L = R * 299/1000 + G * 587/1000 + B * 114/1000
