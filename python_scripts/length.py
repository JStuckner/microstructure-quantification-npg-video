import numpy as np
from scipy.misc import imread, imsave, toimage
from scipy import misc
from stuckpy.microscopy import inout
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import *
from scipy.ndimage.filters import gaussian_filter1d
from skimage.morphology import binary_erosion, remove_small_objects
from skimage.draw import line

in_folder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\align3\segment'
mask = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48/length_mask5.tif'
out_folder = r'E:\E_Documents\Research\NPG\Mechanical Testing\20180307\Movie_41-48\align3\length_plot'
infile = 'fixstamps.txt'

files = inout.get_file_names(in_folder)
files = files[:-60]
#files = files[:200]
times = []

with open(infile, 'r') as f:
    d = dict([line.split() for line in f])

for file in files:
    name = file.split('/')[-1]
    times.append(float(d[name]))
    try:
        if times[-2] > times[-1]:
            #print(times[-2], times[-1])
            times[-1] = times[-2] + 0.1
    except:
        pass
lengths = []
mim = misc.imread(mask, mode='L')
mim = mim > 1

print('getting diameters')
for file in files:
    im = misc.imread(file, mode='L')
    im = im > 1
##    m = np.zeros(im.shape)
##    left = np.where(im[350,:] > 0)
##
##    left = left[0][0]
##    #print(left)
##    x1 = left+300
##    y1 = 0
##    x2 = left-200
##    y2 = 400
##    rr,cc = line(x1,y1,x2,y2)
##    m[rr,cc] = 1
##    if file == files[0] or file == files[100]:
##        print(x1)
##        print((y2-y1)/(x2-x1))
##        plt.imshow(m)
##        plt.show()

    #plt.imshow(m)
    #plt.show()
    #print(left)
    
    
    im =  binary_erosion(im, selem=np.ones((11,11)))
    im = im > 0
    im = remove_small_objects(im, 1000)
    lengths.append(np.count_nonzero(mim[np.where(im==0)]))
##    try:
##        if lengths[-1] < 200 or lengths[-1] > 450:
##            lengths[-1] = lengths[-2]
##    ##        plt.imshow(im)
##    ##        plt.show()
##    ##        plt.imshow(mim)
##    ##        plt.show()
####        if (abs(
####            ((lengths[-1] / lengths[0] * 100)-100) -
####            ((lengths[-2] / lengths[0] * 100)-100)) >
####            8):
####            print(lengths[-1], lengths[-2])
####            lengths[-1] = np.copy(lengths[-2])
####            print(lengths[-2], lengths[-1])
##    except IndexError:
##        print(lengths[-1])

l = [(i / lengths[0] * 100)-100 for i in lengths]
one = l[1482]
two = l[1483]
print([l[i] for i in range(1480, 1490)])
l = gaussian_filter1d(l, sigma=3)
l[1482] = one
l[1483] = two
print('making plots')        
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
ax.set_ylabel('Strain [%]', fontproperties=font_prop, labelpad=3)
#ax.set_xticks(ind + width / 2)
tick_labels = []
ax.tick_params(labelsize=24)

#print(len(times), len(diameters))
my_plot = ax.plot(times, l, lw=2)
plt.tight_layout()

for i, file in enumerate(files):
    point = ax.plot(times[i],l[i], 'go', ms=15, c='orange')
    plt.savefig(file.replace(in_folder, out_folder), dpi=50)
    del ax.lines[1]
