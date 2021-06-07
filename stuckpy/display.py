import numpy as np
import matplotlib.pyplot as plt
from stuckpy.image.text import string_to_array

def append_scale_bar(image, scale):
    rows, cols = image.shape
    white = np.max(image)

    # Add a blank region at the bottom for the meta data
    res_factor = int(rows/1000) # 1 per 1000 pixels of resolution
    scale_height = res_factor * 50 #50 pixels / 1000 pixels of resolution.
    image = np.append(image, np.zeros((scale_height, rows)), axis=0)


    

    # Create a scale bar that is roughly 1/5 the width of the image
    nm_perfect = int(round(cols * scale / 5, 0))
    digits = len(str(nm_perfect))
    div = 10**(digits - 1)
    nm = int(nm_perfect / div) * div
    pixels = round(nm/scale)
    bar = np.zeros((scale_height, pixels))
    brows, bcols = bar.shape
    bar[:,0:res_factor*4] = white
    bar[:, pixels-res_factor*4:pixels] = white
    bar[:int(brows/4),:] = 0
    bar[brows-int(brows/4):,:] = 0
    bar[int(scale_height/2)-res_factor*3+1:
        int(scale_height/2)+res_factor*3,:] = white
    bnumber = ' ' + str(nm) + ' nm'
    arraytext = string_to_array(bnumber, color=white)
    _, acols = arraytext.shape
    atext = np.zeros((50,acols))
    atext[10:40,:] = arraytext
    bar = np.append(bar, atext, axis=1)
    brows, bcols = bar.shape
    left = int(cols/2) - int(bcols/2)
    right = int(cols/2) + int(bcols/2)
    try:
        image[rows:,left:right] = bar
    except ValueError:
        image[rows:,left:right+1] = bar


    #Create a white boarder
    image[rows:rows+res_factor*3, :] = white
    image[rows + scale_height - res_factor*3:rows + scale_height, :] = white
    image[rows:rows+scale_height - 1, 0:res_factor*3] = white
    image[rows:rows+scale_height - 1, cols-res_factor*3:cols] = white


    
    return image
