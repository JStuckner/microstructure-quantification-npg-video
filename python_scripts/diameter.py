import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from scipy.misc import imread, imsave, toimage
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from skimage.morphology import medial_axis, skeletonize
from scipy import ndimage
from skimage.measure import label
from shutil import copyfile

from scipy.signal import convolve2d

#import mahotas as mh
#from mahotas import polygon

from stuckpy.microscopy import inout
from stuckpy.microscopy import visualize
from stuckpy.microscopy import segment




def smoothEdges(mask, smooth_radius=1):

    smooth_radius = max(smooth_radius, 1)

    if round(smooth_radius, 0) > int(smooth_radius): # If round up.
        size = int(smooth_radius + 1)
        selem = disk(round(smooth_radius,0))
    else:
        size = 1 + 2*int(smooth_radius)
        selem = np.ones((size,size))

    smooth_mask = ndimage.binary_opening(mask, structure=selem)
    smooth_mask = ndimage.binary_closing(smooth_mask, structure=selem)

    return smooth_mask

def this_segment(file, in_folder, out_folder):
    imfolder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\cropped'
    vfolder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\diameter_visualize'
    mfolder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\diameter_measure'

    im = imread(file.replace(in_folder, imfolder))


    try:
        mask = imread(file, mode="L")
    except:
        imsave(file.replace(in_folder, vfolder), im)
        return True
    
    mask = mask > 10
    mask = smoothEdges(mask, smooth_radius=7)

    skel, dst = medial_axis(mask, return_distance=True)
    skel = skeletonize(mask)

    #skel[:, 600:] = 0
    #skel[:120, :340] = 0
    
    
    # get ligament and node labels
    nodes = np.copy(skel)
    ligaments = np.copy(skel)
    ends = np.copy(skel)
    neighbors = convolve2d(skel, np.ones((3,3)), mode='same')
    neighbors = neighbors * skel
    nodes[neighbors < 4] = 0
    ligaments[neighbors > 3] = 0
    ends[neighbors != 2] = 0
    edge_lab = label(ligaments, background=0)

    unique, counts = np.unique(edge_lab, return_counts=True)

    terminal = edge_lab * ends

##    plt.imshow(edge_lab)
##    plt.show()
##    plt.imshow(terminal)
##    plt.show()

    for u in np.unique(terminal, return_counts=False):
        #print(u)
        if counts[np.where(unique == u)] < 200:
            skel[np.where(edge_lab == u)] = 0


##    try:
##        for i,u in enumerate(unique):
##            if counts[i] < 100:
##                skel[np.where(edge_lab == u)] = 0
##    except:
##        pass
##    skel[np.where(nodes!=0)] = 0

            
    #print(edge_lab)
    skel = skel*dst
    skel = skel*2
    #skel[:200, :] = 0
    #skel[490:, :] = 0
    #skel[:,500:] = 0
    
    #skel[:,:190] = 0
    imsave(file.replace(in_folder, mfolder), toimage(skel, cmin=0, cmax=255))
    skel[10, 500:700] = [i for i in range(1,201,1)]
    skel[11, 500:700] = [i for i in range(1,201,1)]
    skel[12, 500:700] = [i for i in range(1,201,1)]
    skel[13, 500:700] = [i for i in range(1,201,1)] 
    v = visualize.showSkel(skel, im, dialate=True, notMask = False, returnSkel = True,
                           cmap=plt.cm.viridis)

    
    imsave(file.replace(in_folder, vfolder), v)

    return True

def run():
    if False:
        root = tk.Tk()
        root.withdraw()
        in_folder = filedialog.askdirectory(title='Select input folder')
        out_folder = filedialog.askdirectory(title='Select output folder')
        root.destroy()
    else:
        in_folder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\brittle clip\segment'
        out_folder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\Segment_23'

    files = inout.get_file_names(in_folder)
    #files = files[1500:1700]
    #this_segment(files[2775], in_folder, out_folder)
    job = Parallel(n_jobs=4, verbose=50)(delayed(this_segment)(files[i], in_folder, out_folder) for i in range(len(files)))
    #job = this_segment(files[0], in_folder, out_folder)

if __name__ == '__main__':
    run()
