import numpy as np
from scipy.misc import imread, imrotate, imsave
import matplotlib.pyplot as plt

ims = [i for i in range(11470, 12469, 99)]
ims = ims + [12469, 12472, 12568, 12667]
print(ims)
files = [''.join(('frame', str(i),'.tif')) for i in ims]

for i, f in enumerate(files):
    print(f)
    im0 = imread(f)
    rows, cols = im0.shape
    im = np.zeros((rows+200, cols+200))
    im[100:-100, 100:-100] = im0
    im = imrotate(im, -80)
    im = im[75:475, 200:500]
    imsave(f.replace('frame', 'crop\\frame'), im)
    #plt.imshow(im, cmap=plt.cm.gray)
    #plt.show()
