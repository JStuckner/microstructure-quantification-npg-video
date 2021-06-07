import numpy as np
import skimage.filters
from scipy import ndimage

import stuckpy.microscopy as sm

def triangle(image, sigma=10, thresh_mult = 1.0, filt='gaussian'):
    '''
    Used to segment TEM images.  First apply a large guassian filter and then
    use the histogram based triangle thresholding technique.

    Parameters
    ----------
    image : ndarray (2D)
        TEM image to be segmented.
    sigma : float
        Sigma of Gaussian filter.
    thresh_mult : float
        Adjust the threshold amount.

    Return
    ------
    seg : ndarray (2D)
        Segmented image.
    '''

    # Apply Gaussian filter.
    if filt == 'median':
        image = ndimage.filters.median_filter(image, sigma)
    else:
        image = skimage.filters.gaussian(image, (sigma, sigma))

    # Apply triangle segmentation.
    thresh_value = skimage.filters.threshold_triangle(image)
    seg = image < thresh_value * thresh_mult

    return seg
    
    
    
    
