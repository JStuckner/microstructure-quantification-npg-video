import numpy as np
import matplotlib.pyplot as plt
import warnings

from astropy.modeling import models, fitting
from scipy.misc import imread

def polynomial_fit_normalize(im, mask=None, return_fit=False, dtype='float32',
                             fit_path=None):
    """
    Fits a 3D surface to the inensity of pixels using 2nd order poly fit
    and subtracts the fit from the image to remove trends.
    """
    from astropy.modeling import models, fitting
    rows, cols = im.shape
    y, x = np.mgrid[:rows,:cols]

    if mask is not None:
        m = np.ma.masked_array(im, mask=mask)
    else:
        m = im

    # Fit the data using astropy
    p_init = models.Polynomial2D(degree=2)
    fit_p = fitting.LevMarLSQFitter()
    with warnings.catch_warnings():
        # Ignore model linearity warning from the fitter
        warnings.simplefilter('ignore')
        p = fit_p(p_init, x, y, m)
    fit = p(x,y)

    if fit_path is not None:
        imsave(fit_path, fit.astype('uint8'))

    # subtract fit from image
    
    fit_minus_mean = fit - np.mean(fit)


    
    if dtype == 'uint8':
        im = np.clip(np.subtract(im, fit_minus_mean), 0, 255).astype(dtype)
    else:
        im = np.subtract(im, fit_minus_mean).astype(dtype)
    

    if return_fit:
        return im, fit
    else:
        return im

path = 'test.tif'
im = imread(path, mode='I')
im, fit = polynomial_fit_normalize(im, dtype='uint8', return_fit=True)
plt.imshow(fit)
plt.show()
