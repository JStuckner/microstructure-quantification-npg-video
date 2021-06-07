import warnings

import numpy as numpy

from skimage import morphology
from scipy import ndimage

def remove_small_objects(mask, small_objects=0, small_holes=0):
    """
    Removes small objects (white areas of mask) and small holes (black areas).

    Parameters
    ----------
    mask : 2D array of bool
        Mask showing the area of one phase.
    small_objects : int
        Max area of connected white pixels that will be removed.
    small_holes : int
        Max area of connected black pixels that will be removed.        
        
    Returns
    -------
    out_mask : 2D array of bool
        Mask with small holes and objects removed.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out_mask = morphology.remove_small_objects(mask, small_objects)
        out_mask = ~morphology.remove_small_objects(~out_mask, small_holes)

    return out_mask

def smooth_edges(mask, smooth_radius=1):
    """
    Smoothes the edges of a binary mask.

    Parameters
    ----------
    mask : 2D array of bool
        Mask showing the area of one phase.
    smooth_radius : float64
        The radius of the smoothing operation.  See note below.
        
    Returns
    -------
    smooth_mask : 2D array of bool
        Mask that has been smoothed.

    Notes
    -----
    smooth_radius sets the structure element (selem) for smoothing the edges of
    the masks. If the smooth_rad rounds up the selem is a disk with radius
    rounded up.  If smooth_radius rounds down, selem is a box.

    Radius = 0 - 1.499
    [[1,1,1],
     [1,1,1],
     [1,1,1]]

    Radius = 1.5 - 1.99
    [[0,0,1,0,0],
     [0,1,1,1,0],
     [1,1,1,1,1],   
     [0,1,1,1,0],
     [0,0,1,0,0]]
     
    Radius = 2 - 2.499
    [[1,1,1,1,1],
     [1,1,1,1,1],
     [1,1,1,1,1],   
     [1,1,1,1,1],
     [1,1,1,1,1]]    
    """

    smooth_radius = max(smooth_radius, 1)

    if round(smooth_radius, 0) > int(smooth_radius): # If round up.
        size = int(smooth_radius + 1)
        selem = morphology.disk(round(smooth_radius,0))
    else:
        size = 1 + 2*int(smooth_radius)
        selem = np.ones((size,size))

    # Smooth edges.
    smooth_mask = ndimage.binary_opening(mask, structure=selem)
    smooth_mask = ndimage.binary_closing(smooth_mask, structure=selem)

    return smooth_mask
