import numpy
import numpy.linalg
import scipy
import MDAnalysis
import MDAnalysis.coordinates.TRJ as TRJ
import MDAnalysis.analysis.distances
from scipy.spatial import distance
from numpy import *

#------------------------------------------------------------------------------------#
# Contact Analysis between two selections,
# 0 to 1 (0=never below threshold, 1=always above threshold)
# by M.E. Pitman
#------------------------------------------------------------------------------------#

# Load AMBER trajectory
u = MDAnalysis.Universe("OMAH_2X12mer_corrected_final.parm7", "2X12mer_wat_md2_1000ns.nc", format='NCDF')
timestep = 1
n_frames = len(u.trajectory)
start = 0

# Select the regions to be measured against each other from the trajectory
chain1 = u.select_atoms('resid 1-12').center_of_mass()
chain2 = u.select_atoms('resid 13-24').center_of_mass()

# Determine dimensions of matrix
n1 = len(chain1)
n2 = len(chain2)

# Initialize array with zeros
contact_sum = numpy.zeros((n1, n2))

# Define your max_distance (cutoff, example 5.0)
max_distance = 4.0

# Sum 1 or 0 of each matrix position across timesteps
for ts in u.trajectory[start::timestep]:
    ch1_com = chain1.reshape(-1, 3) # center of mass coordinates of chain1    
    ch2_com = chain2.reshape(-1, 3) # center of mass coordinates of chain2
    ts_dist = distance.cdist(ch1_com, ch2_com, 'euclidean')
    ts_dist[ts_dist < max_distance] = 1
    ts_dist[ts_dist > max_distance] = 0
    contact_sum = ts_dist + contact_sum

contact_ratio = contact_sum / n_frames

# Basic imaging
from pylab import imshow, xlabel, ylabel, xlim, ylim, colorbar, cm, clf
import matplotlib.pyplot as plt

class Formatter(object):
    def __init__(self, im):
        self.im = im
    def __call__(self, x, y):
        z = self.im.get_array()[int(y), int(x)]
        return 'x={:.01f}, y={:.01f}, z={:.01f}'.format(x, y, z)

# Set x_min and y_min to the lowest residue index (example residue 50)
cr_shape = contact_ratio.shape
x_shift = cr_shape[1]
y_shift = cr_shape[0]
x_min = 1
y_min = 13
x_max = x_min + x_shift
y_max = y_min + y_shift

# Set aspect=equal
im = plt.imshow(contact_ratio, vmin=0, vmax=1, aspect='equal', origin='lower', extent=[x_min,x_max, y_min, y_max], cmap='viridis')

im.set_cmap('hot')
plt.grid(b=True, color='#737373')

im.set_interpolation('nearest')
plt.format_coord = Formatter(im)
delta = 1

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

colorbar()
plt.show()