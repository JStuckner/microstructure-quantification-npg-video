import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# get files and output folder
root = tk.Tk()
root.withdraw()
files = filedialog.askopenfilenames(title='Select movies')
out_folder = filedialog.askdirectory(title='Select output folder')
root.destroy()

# save frames
count = 0
scount = 0
for file in files:
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, cols = im.shape
    success,newimage = vidcap.read()
    while success:
        im2 = cv2.cvtColor(newimage, cv2.COLOR_BGR2GRAY)
        n = np.count_nonzero(im==im2)
        if n < rows*cols/4: # meaning that 3/4 of the pixels are different by at least 1 intensity
            im = np.copy(im2)
            c = str(count).zfill(6)
            cv2.imwrite(''.join((out_folder, '\\', "frame_%s.tif" % c)),im)     # save frame
            count += 1
        else:
            scount += 1
            success,newimage = vidcap.read()
        
