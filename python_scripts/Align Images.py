import cv2
from scipy.misc import imread, imsave
import time
import numpy as np
import os
from skimage.feature import register_translation
from scipy.ndimage import filters
import errno
import matplotlib.pyplot as plt
import tifffile as tiff

from stuckpy.microscopy import inout
from stuckpy.microscopy import visualize
from stuckpy.microscopy import operations

INPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Frames\ductile'
OUTPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Frames\ductile align'
TO_REF = True # true = align to reference image, false = align to next image.
REF = 20 #Set to None for middle image
SIGMA = 2 #blur amount
disable_y = False

# Load Images
if True:
    # Load Images
    t = time.time()
    print('Loading images...', end='')
    files = inout.get_file_names(INPUT_FOLDER, 'tif')
    #files = files[500:800]
    im0 = imread(files[0], 'L')
    rows, cols = im0.shape
    num = len(files)
    im = np.zeros((rows,cols,num), dtype='uint8')
    for i, file in enumerate(files):
        im[:,:,i] = imread(files[i], 'L')
    im = im[300:, :,:] # crop 
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)

# Ensure directory exists
try:
    os.makedirs(OUTPUT_FOLDER)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Align Images
if True:
    to_ref = TO_REF #align to middle image (True) or adjacent image (False)
    
    #Preprocess images
    frames = im.copy()
    t = time.time()
    print('Applying Gaussian filter...', end='')
    im = operations.gaussian(im, SIGMA)
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)

    # Calculate shift matrix
    rows,cols,num = im.shape
    ref = int(num/2)
    if REF is not None:
        ref = REF

    plt.imshow(im[:,:,ref], cmap=plt.cm.gray)
    plt.show()
    
    shift = np.zeros((num, 2)) #initialize shift matrix - [y, x] for each image

    if to_ref:
        print('Reference image:', ref, files[ref].split('\\')[-1])
        t = time.time()
        print('Calculating offset for %d images...' %num, end='')
        #align back half first
        for i in range(ref,num-1):
            if i % 10 == 0:
                visualize.update_progress((i-ref)/num)
            shift[i+1,:], _, _ = register_translation(im[:,:,ref], im[:,:,i+1], 10) #calc offset relative to last image
        #now align front half
        for i in range(ref, 0, -1):
            if i % 10 == 0:
                visualize.update_progress((num-i)/num)
            shift[i-1,:], _, _ = register_translation(im[:,:,ref], im[:,:,i-1], 10) #calc offset relative to last image
        elapsed = time.time() - t                     
        print('Done.  Took %.2f seconds.' %elapsed)

        if disable_y:
            shift[:,1] = 0

        # adjust the shift array such that 0,0 is the minumum
        minrow, mincol = np.amin(shift, axis=0)
        maxrow, maxcol = np.amax(shift, axis=0)
        for i in range(num):
            shift[i,0] -= minrow
            shift[i,1] -= mincol

    else:
        t = time.time()
        print('Calculating offset for %d images...' %num, end='')
        for i in range(ref,num-1):
            if i % 10 == 0:
                visualize.update_progress((i-ref)/num)
            shift[i+1,:], _, _ = register_translation(im[:,:,i], im[:,:,i+1], 10) #calc offset relative to last image
            shift[i+1,:] = shift[i+1,:] + shift[i,:] #relative to reference image
        #now align front half
        for i in range(ref, 0, -1):
            if i % 10 == 0:
                visualize.update_progress((num-i)/num)
            shift[i-1,:], _, _ = register_translation(im[:,:,i], im[:,:,i-1], 10) #calc offset relative to last image
            shift[i-1,:] = shift[i-1,:] + shift[i,:] #relative to reference image
        elapsed = time.time() - t                     
        print('Done.  Took %.2f seconds.' %elapsed)

        if disable_y:
            shift[:,1] = 0
            
        # adjust the shift array such that 0,0 is the minumum
        minrow, mincol = np.amin(shift, axis=0)
        maxrow, maxcol = np.amax(shift, axis=0)
        for i in range(num):
            shift[i,0] -= minrow
            shift[i,1] -= mincol

    # Save shift file for reference
    try:
        np.save(SHIFT_FILE, shift)
    except:
        pass

    # get shape of final movie    
    minrow, mincol = np.amin(shift, axis=0)
    maxrow, maxcol = np.amax(shift, axis=0)
    rows = rows + int(round(maxrow))
    cols = cols + int(round(maxcol))

    # Generate shifted images
    t = time.time()
    print('Shifting %d images...' %num, end='')
    #shiftim = []
    shiftim = np.zeros((rows,cols,num), dtype='uint8')
    for i in range(num):
      M = np.float32([[1,0,shift[i,1]],[0,1,shift[i,0]]]) #transformation matrix
      shiftim[:,:,i] = cv2.warpAffine(frames[:,:,i],M,(cols,rows))
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)

    #print(shift)

    # Save images
    if True:
        t = time.time()
        print('Saving %d images...' %num, end='')
        for i in range(num):
            tiff.imsave(files[i].replace(INPUT_FOLDER, OUTPUT_FOLDER), shiftim[:,:,i])
        elapsed = time.time() - t                     
        print('Done.  Took %.2f seconds.' %elapsed)
