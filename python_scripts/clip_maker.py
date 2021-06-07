import cv2
from scipy.misc import imread, imsave
import time
import numpy as np
import os
import h5py
from skimage.feature import register_translation

from stuckpy.microscopy import inout
from stuckpy.microscopy import visualize
from stuckpy.microscopy import operations

# Step 1 - Save Frames

step1 = False
if step1:
  print('working on step 1')
  vidcap = cv2.VideoCapture('Cropped.mp4')
  success,image = vidcap.read()
  count = 0
  success = True
  while success:
    success,image = vidcap.read()
    #print('Read a new frame: ', success)
    try:
      c = str(count).zfill(6)
      cv2.imwrite("Frames//frame{}.tif".format(c), cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))     # save frame as JPEG file
      count += 1    
    except:
      pass

# Step 1a - Add zeroes beginning of frame number for alphebetizing in order
step1a = False
if step1a:
  for i, file in enumerate(inout.files_in_subfolders(r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip1\Raw', 'tif')):
    f = file.split('\\')[-1]
    if len(f) == 13:
      os.rename(file, ''.join((str(file[:-8]), '0', str(file[-8:]))))

# Step 2 - crop images
step2 = False
if step2:
  print('working on step 2')
  for file in inout.files_in_subfolders('Frames', 'tif'):
    im = imread(file, 'L')
    im = im[26:1073, 196:1242]
    try:
      imsave(file, im)
    except:
      print('Failed to crop', file)

#Step 2a - delete copied frames
step2a = False
if step2a:
  for i, file in enumerate(inout.files_in_subfolders(r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip3\Frames', 'tif')):
    
    if i > 0:
      im1 = imread(file, mode='L')
      f1 = file.split('\\')[-1]
      c = np.count_nonzero(im0==im1)
      #eq = np.array_equal(im0, im1)
      if c > 100000:
        print('{} same as {}.'.format(f1, f0))
        os.remove(file)
      #else:
        #print('')
      im0 = im1.copy()
      f0 = f1
    else:
      im0 = imread(file, mode='L')
      f0 = file.split('\\')[-1]
    


# Step 2b - crop some more from hdf5 file
step2b = False
if step2b:
  # load hdf5
  file = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\Frames/clip2.hdf5'
  f = h5py.File(file, "r")
  frames = f['data'][()]

  #crop
  frames = frames[200:, :990,:]

  #save
  rows, cols, num_frames = frames.shape
  with h5py.File(file.replace('clip2.hdf5', 'clip2_cropped.hdf5'), 'w') as f:
    dset = f.create_dataset("data", (rows,cols,num_frames), data=frames)
  

  
# Step 3 - align images
step3 = True
if step3:
  print('working on step 3')

  # Read images from hdf5 file
  t = time.time()
  print('Reading images...', end='')
  # load hdf5
  file = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\Frames/Clip2_cropped3.hdf5'
  f = h5py.File(file, "r")
  frames = f['data'][()]
  elapsed = time.time() - t                     
  print('Done.  Took %.2f seconds.' %elapsed)
  
  #Preprocess images
  #frames = frames[:,:,750:780]
  im = frames.copy()
  im = operations.gaussian(im, sigma=1)
  
  
  # Calculate shift matrix
  rows,cols,num = im.shape
  ref = int(num/2)
  #cv2.imshow('image',im[:,:,ref])
  #cv2.waitKey(0)
  #ref = 1150
  shift = np.zeros((num, 2)) #initialize shift matrix - [y, x] for each image

  #align back half first
  to_ref = True
  if to_ref:
    t = time.time()
    print('Calculating offset for %d images...' %num, end='')
    for i in range(ref,num-1):
        if i % 10 == 0:
            visualize.update_progress((i-ref)/num)
        shift[i+1,:], _, _ = register_translation(im[:,:,ref], im[:,:,i+1], 10) #calc offset relative to last image
    #now align front half
    for i in range(ref, 0, -1):
        if i % 10 == 0:
            visualize.update_progress((num-i)/num)
        shift[i-1,:], _, _ = register_translation(im[:,:,ref], im[:,:,i-1], 10) #calc offset relative to last image
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)

    # adjust the shift array such that 0,0 is the minumum
    minrow, mincol = np.amin(shift, axis=0)
    maxrow, maxcol = np.amax(shift, axis=0)
    for i in range(num):
        shift[i,0] -= minrow
        shift[i,1] -= mincol

  else:
    t = time.time()
    print('Calculating offset for %d images...' %num, end='')
    for i in range(ref,num-1):
        if i % 10 == 0:
            visualize.update_progress((i-ref)/num)
        shift[i+1,:], _, _ = register_translation(im[:,:,i], im[:,:,i+1], 10) #calc offset relative to last image
        shift[i+1,:] = shift[i+1,:] + shift[i,:] #relative to reference image
    #now align front half
    for i in range(ref, 0, -1):
        if i % 10 == 0:
            visualize.update_progress((num-i)/num)
        shift[i-1,:], _, _ = register_translation(im[:,:,i], im[:,:,i-1], 10) #calc offset relative to last image
        shift[i-1,:] = shift[i-1,:] + shift[i,:] #relative to reference image
    elapsed = time.time() - t                     
    print('Done.  Took %.2f seconds.' %elapsed)

    # adjust the shift array such that 0,0 is the minumum
    minrow, mincol = np.amin(shift, axis=0)
    maxrow, maxcol = np.amax(shift, axis=0)
    for i in range(num):
        shift[i,0] -= minrow
        shift[i,1] -= mincol

  sfile = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\shift_ref_gauss1.npy'
  np.save(sfile, shift)
  
  # get shape of final movie    
  minrow, mincol = np.amin(shift, axis=0)
  maxrow, maxcol = np.amax(shift, axis=0)
  rows = rows + int(round(maxrow))
  cols = cols + int(round(maxcol))

  # Generate shifted images
  out_path = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\Aligned8.hdf5'
  t = time.time()
  print('Shifting %d images...' %num, end='')
  #shiftim = []
  shiftim = np.zeros((rows,cols,num), dtype='uint8')
  for i in range(num):
      M = np.float32([[1,0,shift[i,1]],[0,1,shift[i,0]]]) #transformation matrix
      #shiftim = cv2.warpAffine(frames[:,:,i],M,(cols,rows))
      shiftim[:,:,i] = cv2.warpAffine(frames[:,:,i],M,(cols,rows))
      #imsave(''.join((out_path, '/', str(i).zfill(5), '.tif')), shiftim)
  with h5py.File(out_path, 'w') as f:
      dset = f.create_dataset("data", (rows,cols,num), data=shiftim)
  elapsed = time.time() - t                     
  print('Done.  Took %.2f seconds.' %elapsed)

#step 3a load shift matrix
step3a = False
if step3a:

  print('working on step 3a')

  # Read images from hdf5 file
  t = time.time()
  print('Reading images...', end='')
  # load hdf5
  file = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\Frames/Clip2_cropped3.hdf5'
  f = h5py.File(file, "r")
  frames = f['data'][()]
  elapsed = time.time() - t                     
  print('Done.  Took %.2f seconds.' %elapsed)
  
  #Preprocess images
  #frames = frames[:,:,750:780]
  im = frames.copy()
  #im = operations.gaussian(im, sigma=0.5)
  
  
  # Calculate shift matrix
  rows,cols,num = im.shape
  
  sfile = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\shift.npy'
  shift = np.load(sfile)

  # get shape of final movie    
  minrow, mincol = np.amin(shift, axis=0)
  maxrow, maxcol = np.amax(shift, axis=0)
  rows = rows + int(round(maxrow))
  cols = cols + int(round(maxcol))
  
  # Generate shifted images
  out_path = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\Aligned6.hdf5'
  t = time.time()
  print('Shifting %d images...' %num, end='')
  #shiftim = []
  shiftim = np.zeros((rows,cols,num), dtype='uint8')
  for i in range(num):
      M = np.float32([[1,0,shift[i,1]],[0,1,shift[i,0]]]) #transformation matrix
      #shiftim = cv2.warpAffine(frames[:,:,i],M,(cols,rows))
      shiftim[:,:,i] = cv2.warpAffine(frames[:,:,i],M,(cols,rows))
      #imsave(''.join((out_path, '/', str(i).zfill(5), '.tif')), shiftim)
  with h5py.File(out_path, 'w') as f:
      dset = f.create_dataset("data", (rows,cols,num), data=shiftim)
  elapsed = time.time() - t                     
  print('Done.  Took %.2f seconds.' %elapsed) 

# step4 - crop and save movie
step4 = False
if step4:
  t = time.time()
  print('Reading images...', end='')
  # load hdf5
  file = r'E:\E_Documents\Research\NPG\Mechanical Testing\20171214 TEM tensile success\Movie 1\Clip2\Aligned6.hdf5'
  f = h5py.File(file, "r")
  frames = f['data'][()]
  elapsed = time.time() - t                     
  print('Done.  Took %.2f seconds.' %elapsed)

  #Crop
  #frames = frames[500:1200,500:1450,:]

  inout.save_movie(frames, 'Clip2_1.mp4', fps=10, bit_rate=5000)
