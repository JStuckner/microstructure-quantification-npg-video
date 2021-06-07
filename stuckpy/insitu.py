import numpy as np
import cv2
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Tk

def movies_to_frames(movie_path=None, out_folder=None, sameness_thresh=0.25,
                     digits=5):
    """
    Seperates all frames in the movie and puts them in the out_put folder

    movie_path : path to movie
    output_folder : folder to put frames
    sameness_thresh : minimum fraction of pixels that need to be different
                      from one frame to the next to keep the frame.
    digits : how many digits in the frame index
    """

    Tk().withdraw() # hide the annoying window behind the filedailog.

    # Check inputs
    if sameness_thresh > 1 or sameness_thresh < 0:
        raise ValueError("sameness_threshold should be between 0 and 1.")
        sys.exit()
    
    if movie_path is None:
        ftypes = [
            ('Movies', '*.avi;*.mp4;*.wmv;*.mov;*.flv'), #semicolon trick
            ('All files', '*')
            ]
        movie_path = fd.askopenfilename(title="Select Movie", filetypes=ftypes) 
        
    try:
        vidcap = cv2.VideoCapture(movie_path)
        success,image = vidcap.read()
        if not success:
            raise RuntimeError("Failed to load movie.  Check file path.")
            sys.exit()
    except:
        raise RuntimeError("Failed to load movie.  Check file path.")
        sys.exit()

    if out_folder is None:
        out_folder = fd.askdirectory(
            title="Select output folder")
        if out_folder is None or out_folder=="":
            raise RuntimeError("No output folder selected")
            sys.exit()
            
    # Prepare
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, cols = im.shape
    count = 0
    skipped_count = 0

    # Start saving
    print("Saving frames...")
    c = str(count).zfill(digits)
    cv2.imwrite(''.join((out_folder, '\\', "frame%s.tif" % c)),im) # save first
    success,newimage = vidcap.read()
    while success:
        im2 = cv2.cvtColor(newimage, cv2.COLOR_BGR2GRAY)
        n = np.count_nonzero(im==im2)
        # if fraction of pixels less than threshold are the same.
        if n < rows*cols*sameness_thresh: 
            count += 1
            im = np.copy(im2)
            c = str(count).zfill(digits)
            cv2.imwrite(''.join((out_folder, '\\', "frame%s.tif" % c)),im)
        else:
            skipped_count += 1
        success,newimage = vidcap.read()

    print("Frames saved. Skipped", skipped_count, "frames that were the same.")

if __name__ == "__main__":
    movies_to_frames()
