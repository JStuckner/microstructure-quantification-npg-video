import numpy as np
from scipy.misc import imread, imsave, imresize
from joblib import Parallel, delayed
from pytesseract import image_to_string
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

from stuckpy.microscopy import inout

INPUT_FOLDER = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\Frames'
outfile = 'timestamps.txt'


def get_time_stamps(file):
    im = imread(file, mode='L')
    im = im[1001:1017, 926:987]
    im = imresize(im, 300)
    im = Image.fromarray(np.uint8(plt.cm.gist_earth(im)*255))
    #plt.imshow(im)
    #plt.show()
    strTime = image_to_string(im)

        
    
    #minutes = strTime[2:4]
    #seconds = strTime[5:7]

    try:
        hours, minutes, seconds = strTime.split(':')
        time = float(hours)*3600 + float(minutes)*60 + float(seconds) - 13962.0
    except ValueError:
        time = -1
    
    
    return time

def run():
    files = inout.get_file_names(INPUT_FOLDER, 'tif')
    #files = files[:20]
    time = []
    time = Parallel(n_jobs=4, verbose=10)(delayed(get_time_stamps)(file) for file in files)
    
    t = 0

    for i in range(len(time)):
        if time[i] == -1:
            time[i] = time[i-1]

##    unique, counts = np.unique(time, return_counts=True)
##
##            
##    for i, u in enumerate(unique):
##        for j in range(counts[i]):
##            time[t] = time[t] + (j / counts[i])
##            t += 1

    with open(outfile, 'w') as f:
        for i, t in enumerate(time):
            name = files[i].split('\\')[-1]
            out = ''.join((name, ' ', str(t), '\n'))
            f.write(out)

if __name__ == '__main__':
    run()
