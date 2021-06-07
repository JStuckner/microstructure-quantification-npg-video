import tifffile as tiff
from scipy.misc import imread, imsave
import numpy as np
import os
from stuckpy.microscopy import inout
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import *
from joblib import Parallel, delayed

INPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\align3\diameter_measure'
OUTPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\align3\diameter_plot'
infile = 'fixstamps.txt'


def run():
    # get diameters from frames
    files = inout.get_file_names(INPUT_FOLDER, 'tif')
    files = files[:-51]
    diameters = []
    for file in files:
        im = imread(file)
        im = im[400:550, 100:300]
        #plt.imshow(im)
        #plt.show()
        nonzero = im[np.nonzero(im)]
        try:
            diameters.append(np.min(im[np.nonzero(im)]))
        except:
            print('skipping', file)
            diameters.append(diameters[-1])
    diameters = [round(float(i) * 0.0833, 2) for i in diameters]
    times = []

    with open(infile, 'r') as f:
        d = dict([line.split() for line in f])

    for file in files:
        name = file.split('\\')[-1]
        times.append(float(d[name]))
        try:
            if times[-2] > times[-1]:
                #print(times[-2], times[-1])
                times[-1] = times[-2] + 0.1
        except:
            pass

    print(len(diameters), len(times))
    for d, t in zip(diameters, times):
        if d > 10 and t > 400:
            d = 8.75
        #print(d, t)
    
    #times = [i/10 for i in range(0, len(files))]

    # plot setup
    font_path = 'C:\Windows\Fonts\Arial.ttf'
    font_prop = font_manager.FontProperties(fname=font_path, size=30)
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)

    #Set tick spacing before you create a fig!!
    pylab.rcParams['xtick.major.pad']='3'
    pylab.rcParams['ytick.major.pad']='3'

    # Set grid size
    gs = plt.GridSpec(1, 1)  # a 1x1 grid
    fig = plt.figure(figsize=(7, 7))  # figure size in inches

    #Define subplots. Can add as many as you want:
    ax = plt.subplot(1,1,1)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Limit the range of the plot to only where the data is.
    #ylim(40,120)
    #xlim(0,500)

    # Add some text for labels, title and axes ticks.
    ax.set_xlabel('Time [s]', fontproperties=font_prop, labelpad=3)
    ax.set_ylabel('Diameter [nm]', fontproperties=font_prop, labelpad=3)
    #ax.set_xticks(ind + width / 2)
    tick_labels = []
    ax.tick_params(labelsize=24)

    #print(len(times), len(diameters))
    my_plot = ax.plot(times, diameters, lw=2)
    plt.tight_layout()

    for i, file in enumerate(files):
        point = ax.plot(times[i],diameters[i], 'go', ms=15, c='orange')
        plt.savefig(file.replace(INPUT_FOLDER, OUTPUT_FOLDER), dpi=50)
        del ax.lines[1]

    


    
def save_plot(file, ax, t, d):
    point = ax.plot(t, d, 'go', ms=15, c='orange')
    plt.savefig(file.replace(INPUT_FOLDER, OUTPUT_FOLDER), dpi=50)
    del ax.lines[1]
    return True

if __name__ == '__main__':
    run()
