import cv2
import matplotlib.pyplot as plt
from scipy.misc import imread, imsave, imresize
import time
import numpy as np
import os
from skimage.feature import register_translation
from scipy.ndimage import filters
import errno
import tifffile as tiff
from joblib import Parallel, delayed

from stuckpy.microscopy import inout
from stuckpy.microscopy import visualize
from stuckpy.microscopy import operations


def level(im, i, file, inFolder, outFolder):
    print(i)
    mask = np.ones(im.shape,dtype='bool')
    m = imread(r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48/mask.tif', 'L')
    mask[m > 250] = False
    #plt.imshow(mask)
    #plt.show()
    fp = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\fit'
    fitpath = ''.join((fp, '/', str(i), '.tif'))
    #im = np.ma.masked_array(im, mask=mask)
    #plt.imshow(im)
    #plt.show()
    levelim = operations.polynomial_fit_normalize(im, mask=m, dtype='uint8', fit_path=fitpath)
    tiff.imsave(file.replace(inFolder, outFolder), levelim)
    return True



def run():
    INPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\Frames'
    OUTPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\Level'
    RESIZE = 1 #set to fraction of desired size.  

    # Load Images
    t = time.time()
    print('Loading images...', end='')
    files = inout.get_file_names(INPUT_FOLDER, 'tif')
    files = files[:10]
    im0 = imread(files[0], 'L')
    rows, cols = im0.shape
    num = len(files)
    im = np.zeros((rows,cols,num), dtype='uint8')
    for i, file in enumerate(files):
        im[:,:,i] = imread(files[i], 'L')
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)


    # Ensure directory exists
    try:
        os.makedirs(OUTPUT_FOLDER)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Level images
    t = time.time()
    print('Leveling images...', end='')

##    for i in range(num):
##        if i % 2 == 0:
##            visualize.update_progress((i)/num)
##
##        thisim = im[:,:,i]
##        levelim = operations.polynomial_fit_normalize(thisim)
##        tiff.imsave(files[i].replace(INPUT_FOLDER, OUTPUT_FOLDER), levelim)
        
    job = Parallel(n_jobs=4, verbose=50)(delayed(level)(im[:,:,i],i,files[i],INPUT_FOLDER,OUTPUT_FOLDER) for i in range(num))
        
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)

if __name__ == '__main__':
    run()
