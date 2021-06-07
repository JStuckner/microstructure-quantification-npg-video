import tifffile as tiff
from scipy.misc import imread, imsave
import numpy as np
import os
from stuckpy.microscopy import inout
from joblib import Parallel, delayed

def crop(file, INPUT_FOLDER):
    OUTPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\cropped'
    im = imread(file, mode='L')
    im = im[420:1020, 325:1050]
    imsave(file.replace(INPUT_FOLDER, OUTPUT_FOLDER), im)
    
def run():
    INPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\aligned'
    
    files = inout.get_file_names(INPUT_FOLDER, 'tif')
    job = Parallel(n_jobs=4, verbose=50)(delayed(crop)(files[i], INPUT_FOLDER) for i in range(len(files)))
    

if __name__ == '__main__':
    run()
