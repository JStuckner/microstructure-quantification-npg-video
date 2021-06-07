import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from skimage.morphology import remove_small_objects, remove_small_holes, binary_erosion, binary_dilation

from stuckpy.microscopy import inout
from stuckpy.microscopy import visualize
from stuckpy.microscopy import segment

def this_segment(file, in_folder, out_folder):
    im = imread(file, mode="L")
    #im[im==0] = 255
    seg = segment.triangle(im, sigma=11, thresh_mult=.95, filt='gaussian')
    #seg[:180, :150] = 0
    
    seg = remove_small_objects(seg, 30000)
    seg = remove_small_holes(seg, 10000)
    #seg = binary_dilation(seg, selem=np.ones((11,11)))
    #seg =  binary_erosion(seg, selem=np.ones((11,11)))
    
    imsave(file.replace(in_folder, out_folder), seg)
    return True

def run():
    if False:
        root = tk.Tk()
        root.withdraw()
        in_folder = filedialog.askdirectory(title='Select input folder')
        out_folder = filedialog.askdirectory(title='Select output folder')
        root.destroy()
    else:
        in_folder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\cropped'
        out_folder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\segment_length'

    files = inout.get_file_names(in_folder)
    #files = files[650:]

    job = Parallel(n_jobs=4, verbose=50)(delayed(this_segment)(files[i], in_folder, out_folder) for i in range(len(files)))

if __name__ == '__main__':
    run()
