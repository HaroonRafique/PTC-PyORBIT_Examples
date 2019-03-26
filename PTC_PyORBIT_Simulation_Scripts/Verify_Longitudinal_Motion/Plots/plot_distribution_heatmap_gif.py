## Move this file to the bunch_output directory to use
# Plots a gif of the distribution evolutions with histograms:
# x-y x-xp y-yp z-dE (no histogram)
# z-dE
# x-y
# x-xp
# y-yp
# Over many turns.
# Uses all files in a directory with a .mat extension
# This includes subdirectories so please be careful.
# As this script saves all file data in a dictionary this script can be 
# slow for many files/particles/turns etc

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 
import os
import sys
#from mpl_toolkits.mplot3d import axes3d
import matplotlib.gridspec as gridspec

# For GIFs - try using the following command to install (on LXPlus)
# pip install --user imageio
import imageio

###################
# Figure settings #
###################

plt.rcParams['figure.figsize'] = [4.0, 3.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.handlelength'] = 5

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

#####################################################
# Loop over files to save file data in a dictionary #
#####################################################

rootdir = os.getcwd()		# Get current working directory

def check_and_make_directory(directory_name):
	if os.path.isdir(directory_name):
		print '\n\tWARNING: in function check_and_make_directory: directory', directory_name,' already exists.\n\tThis directory should be empty to avoid GIF bugs. Exiting function.\n\n'
	else:
		os.mkdir(directory_name)
	return

check_and_make_directory('Gif_all')
check_and_make_directory('Gif_z_dE')
check_and_make_directory('Gif_x_y')
check_and_make_directory('Gif_x_xp')
check_and_make_directory('Gif_y_yp')

extensions = ('.mat')		# All outputs are .mat files
d = dict()
	
iterators = []				# Integers (turn) used to iterate over files

max_file_no = 0
min_file_no = 1E6
min_file = str()
max_file = str()

# Saved figure names used for GIF
fileno = int(1)
filenames_all = []				
filenames_z_dE = []				
filenames_x_y = []				
filenames_x_xp = []				
filenames_y_yp = []				

x_max = 0.
xp_max = 0.
y_max = 0.
yp_max = 0.
z_max = 0.
dE_max = 0.
x_min = 0.
xp_min = 0.
y_min = 0.
yp_min = 0.
z_min = 0.
dE_min = 0.

print '\nIterate over files:\n'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))        # full path to file
            filename = file.replace('_','.')            # replace _ with a .
            fileno = int(filename.split('.')[1])        # use turn number as a key
            iterators.append(fileno)
            if (fileno <= min_file_no):                  # find min turn
                min_file_no = fileno
                min_file = file
            elif (fileno >= max_file_no):                # find max turn
                max_file_no = fileno
                max_file = file
            
            d[fileno]={}                                # append empty turn to dictionary
            sio.loadmat(file, mdict=d[fileno])          # load the data from file  
            
            # Find Max and Min values for plots
            if max(d[fileno]['particles']['x'][0][0][0]) > x_max : x_max = max(d[fileno]['particles']['x'][0][0][0])            
            if max(d[fileno]['particles']['xp'][0][0][0]) > xp_max : xp_max = max(d[fileno]['particles']['xp'][0][0][0])            
            if max(d[fileno]['particles']['y'][0][0][0]) > y_max : y_max = max(d[fileno]['particles']['y'][0][0][0])            
            if max(d[fileno]['particles']['yp'][0][0][0]) > yp_max : yp_max = max(d[fileno]['particles']['yp'][0][0][0])            
            if max(d[fileno]['particles']['z'][0][0][0]) > z_max : z_max = max(d[fileno]['particles']['z'][0][0][0])            
            if max(d[fileno]['particles']['dE'][0][0][0]) > dE_max : dE_max = max(d[fileno]['particles']['dE'][0][0][0])
            if min(d[fileno]['particles']['x'][0][0][0]) < x_min : x_min = min(d[fileno]['particles']['x'][0][0][0])            
            if min(d[fileno]['particles']['xp'][0][0][0]) < xp_min : xp_min = min(d[fileno]['particles']['xp'][0][0][0])            
            if min(d[fileno]['particles']['y'][0][0][0]) < y_min : y_min = min(d[fileno]['particles']['y'][0][0][0])            
            if min(d[fileno]['particles']['yp'][0][0][0]) < yp_min : yp_min = min(d[fileno]['particles']['yp'][0][0][0])            
            if min(d[fileno]['particles']['z'][0][0][0]) < z_min : z_min = min(d[fileno]['particles']['z'][0][0][0])            
            if min(d[fileno]['particles']['dE'][0][0][0]) < dE_min : dE_min = min(d[fileno]['particles']['dE'][0][0][0])
            
print '\nThe first turn recorded is turn ', min_file_no+1, ' in file ', min_file
print '\nThe last turn recorded is turn ', max_file_no+1, ' in file ', max_file

print '\nz_max = ', z_max, ', z_min = ', z_min
print '\ndE_max = ', dE_max, ', dE_min = ', dE_min
print '\n'

z_max = 50.
z_min = -50.

x_max = 1.1* x_max
xp_max = 1.1* xp_max
y_max = 1.1* y_max
yp_max = 1.1* yp_max
z_max = 1.1* z_max
dE_max = 1.1* dE_max
x_min = 1.1* x_min
xp_min = 1.1* xp_min
y_min = 1.1* y_min
yp_min = 1.1* yp_min
z_min = 1.1* z_min
dE_min = 1.1* dE_min

bin_size_x = 128
bin_size_y = 128
bin_size_xp = 128
bin_size_yp = 128
bin_size_z = 128
bin_size_dE = 128

# Loop Over turns, output one file for each turn
for t in sorted(iterators):
	
	print 'Plotting turn ', t

	fig1=plt.figure(figsize=(6,10),constrained_layout=True)
	plt.clf()
	ax1 = fig1.add_subplot(321) 
	ax2 = fig1.add_subplot(322)
	ax3 = fig1.add_subplot(323) 
	ax4 = fig1.add_subplot(324)
	ax5 = fig1.add_subplot(325) 
	ax6 = fig1.add_subplot(326)

	#fig1.subplots_adjust(wspace=width between plots, hspace=height between plots, left=margin, right=margin, top=margin, bottom=margin)
	fig1.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.99, top=0.95, bottom=0.05)
	
	# Create heatmap
	heatmap, xedges, yedges = np.histogram2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['y'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[x_min, x_max],[y_min, y_max]])
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
	# ~ ax1.imshow(heatmap, extent=extent, aspect=( (x_min - x_max)/(y_min - y_max) ) )
	ax1.imshow(heatmap, extent=extent, aspect=1)

	# ~ ax1.legend();
	ax1.set_xlabel('x [m]');
	ax1.set_ylabel('y [m]');
	# ~ ax1.set_xlim(x_min, x_max)
	# ~ ax1.set_ylim(y_min, y_max)
	tit1 = 'X Y Turn = ' + str(t)
	ax1.set_title(tit1);
	ax1.grid(True);

	heatmap2, xedges2, yedges2 = np.histogram2d(d[t]['particles']['xp'][0][0][0], d[t]['particles']['yp'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[xp_min, xp_max],[yp_min, yp_max]])
	extent2 = [xedges2[0], xedges2[-1], yedges2[0], yedges2[-1]]
	# ~ ax2.imshow(heatmap2, extent=extent2, aspect=( (xp_min - xp_max)/(yp_min - yp_max) ))
	ax2.imshow(heatmap, extent=extent, aspect=1)

	ax2.set_xlabel('xp []');
	ax2.set_ylabel('yp []');
	# ~ ax2.set_xlim(xp_min, xp_max)
	# ~ ax2.set_ylim(yp_min, yp_max)
	tit2 = 'XP YP Turn = ' + str(t)
	ax2.set_title(tit2);
	ax2.grid(True);

	heatmap3, xedges3, yedges3 = np.histogram2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['xp'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[x_min, x_max],[xp_min, xp_max]])
	extent3 = [xedges3[0], xedges3[-1], yedges3[0], yedges3[-1]]
	# ~ ax3.imshow(heatmap3, extent=extent3, aspect=( (x_min - x_max)/(xp_min - xp_max) ))	
	ax3.imshow(heatmap, extent=extent, aspect=1)
	
	ax3.set_xlabel('x [m]');
	ax3.set_ylabel('xp []');	
	# ~ ax3.set_xlim(x_min, x_max)
	# ~ ax3.set_ylim(xp_min, xp_max)
	tit3 = 'X XP Turn = ' + str(t)
	ax3.set_title(tit3);
	ax3.grid(True);

	heatmap4, xedges4, yedges4 = np.histogram2d(d[t]['particles']['y'][0][0][0], d[t]['particles']['yp'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[y_min, y_max],[yp_min, yp_max]])
	extent4 = [xedges4[0], xedges4[-1], yedges4[0], yedges4[-1]]
	# ~ ax4.imshow(heatmap4, extent=extent4, aspect=( (y_min - y_max)/(yp_min - yp_max) ))
	ax4.imshow(heatmap, extent=extent, aspect=1)

	ax4.set_xlabel('y [m]');
	ax4.set_ylabel('yp []');
	# ~ ax4.set_xlim(y_min, y_max)
	# ~ ax4.set_ylim(yp_min, yp_max)	
	tit4 = 'Y YP Turn = ' + str(t)
	ax4.set_title(tit4);
	ax4.grid(True);

	# ~ ax5.scatter(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], color='g', label='1.3 eVs');
	heatmap5, xedges5, yedges5 = np.histogram2d(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[z_min, z_max],[dE_min, dE_max]])
	extent5 = [xedges5[0], xedges5[-1], yedges5[0], yedges5[-1]]
	# ~ ax5.imshow(heatmap5, extent=extent5, aspect=( (z_min - z_max)/(dE_min - dE_max) ))
	ax5.imshow(heatmap, extent=extent, aspect=1)

	ax5.set_xlabel('z [m]');
	ax5.set_ylabel('dE [GeV]');
	# ~ ax5.set_xlim(z_min, z_max)
	# ~ ax5.set_ylim(dE_min, dE_max)
	tit5 = 'Z dE Turn = ' + str(t)
	ax5.set_title(tit5);
	ax5.grid(True);

	ax6.scatter(0,0,color='m')

	lab = 'TURN = ' + str(t)
	legend_elements = [Line2D([0], [0], marker='o', color='w', label=lab, markerfacecolor='m', markersize=15)]

	ax6.legend(handles=legend_elements, loc='center')

	figname = 'Gif_all/all_'+ str(t) + '.png'
	fig1.savefig(figname);
	filenames_all.append(figname)
	plt.close()
	
#######################
# 2nd plot for z - dE #
#######################


	fig2 = plt.figure(1)
	gridspec.GridSpec(3,3)				# Create grid to resize subplots
	fig2.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	fig2.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
	tit1 = 'Z dE Turn = ' + str(t)
	
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
	plt.hist(d[t]['particles']['z'][0][0][0], bins = bin_size_z,  range = [z_min, z_max], density=True)
	plt.ylabel('Frequency')
	plt.title(tit1)
	
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], bin_size_z, range=[[z_min, z_max],[dE_min, dE_max]])
	plt.xlabel('z [m]')
	plt.ylabel('dE [GeV]')
	
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
	plt.hist(d[t]['particles']['dE'][0][0][0], bins = bin_size_dE,  range = [dE_min, dE_max], density=True, orientation=u'horizontal')
	plt.xlabel('Frequency')
	current_axis = plt.gca()
	current_axis.axes.get_yaxis().set_visible(False)

	figname = 'Gif_z_dE/z_dE_'+ str(t) + '.png'
	fig2.savefig(figname);
	filenames_z_dE.append(figname)
	plt.close()	
	
######################
# 3rd plot for x - y #
######################
	
	fig3 = plt.figure(1)
	gridspec.GridSpec(3,3)				# Create grid to resize subplots
	fig3.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	fig3.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
	tit1 = 'x y Turn = ' + str(t)
	
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
	plt.hist(d[t]['particles']['x'][0][0][0], bins = bin_size_x,  range = [x_min, x_max], density=True)
	plt.ylabel('Frequency')
	plt.title(tit1)
	
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['y'][0][0][0], bin_size_x, range=[[x_min, x_max],[y_min, y_max]])
	plt.xlabel('x [m]')
	plt.ylabel('y [m]')
	
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
	plt.hist(d[t]['particles']['y'][0][0][0], bins = bin_size_y,  range = [y_min, y_max], density=True, orientation=u'horizontal')
	plt.xlabel('Frequency')
	current_axis = plt.gca()
	current_axis.axes.get_yaxis().set_visible(False)

	figname = 'Gif_x_y/x_y_'+ str(t) + '.png'
	fig3.savefig(figname);
	filenames_x_y.append(figname)
	plt.close()	
	
######################
# 4th plot for x - xp #
######################
	
	fig4 = plt.figure(1)
	gridspec.GridSpec(3,3)				# Create grid to resize subplots
	fig4.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	fig4.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
	tit1 = 'x xp Turn = ' + str(t)
	
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
	plt.hist(d[t]['particles']['x'][0][0][0], bins = bin_size_x,  range = [x_min, x_max], density=True)
	plt.ylabel('Frequency')
	plt.title(tit1)
	
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['xp'][0][0][0], bin_size_x, range=[[x_min, x_max],[xp_min, xp_max]])
	plt.xlabel('x [m]')
	plt.ylabel('xp [rad]')
	
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
	plt.hist(d[t]['particles']['xp'][0][0][0], bins = bin_size_xp,  range = [xp_min, xp_max], density=True, orientation=u'horizontal')
	plt.xlabel('Frequency')
	current_axis = plt.gca()
	current_axis.axes.get_yaxis().set_visible(False)

	figname = 'Gif_x_xp/x_xp_'+ str(t) + '.png'
	fig4.savefig(figname);
	filenames_x_xp.append(figname)
	plt.close()	
	
######################
# 5th plot for y - yp #
######################
	
	fig5 = plt.figure(1)
	gridspec.GridSpec(3,3)				# Create grid to resize subplots
	fig5.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	fig5.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
	tit1 = 'y yp Turn = ' + str(t)
	
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
	plt.hist(d[t]['particles']['y'][0][0][0], bins = bin_size_y,  range = [y_min, y_max], density=True)
	plt.ylabel('Frequency')
	plt.title(tit1)
	
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(d[t]['particles']['y'][0][0][0], d[t]['particles']['yp'][0][0][0], bin_size_y, range=[[y_min, y_max],[yp_min, yp_max]])
	plt.xlabel('y [m]')
	plt.ylabel('yp [rad]')
	
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
	plt.hist(d[t]['particles']['yp'][0][0][0], bins = bin_size_yp,  range = [yp_min, yp_max], density=True, orientation=u'horizontal')
	plt.xlabel('Frequency')
	current_axis = plt.gca()
	current_axis.axes.get_yaxis().set_visible(False)

	figname = 'Gif_y_yp/y_yp_'+ str(t) + '.png'
	fig5.savefig(figname);
	filenames_y_yp.append(figname)
	plt.close()	
	
#############
# Make GIFs #
#############

print '\nCreating x-y x-xp y-yp z-dE (no histogram) GIF'
images = []
for filename in filenames_all:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_all/all.gif', images)	

print 'Creating z - dE GIF'
images = []
for filename in filenames_z_dE:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_z_dE/z_dE.gif', images)	

print 'Creating x - y GIF'
images = []
for filename in filenames_x_y:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_x_y/x_y.gif', images)	

print 'Creating x - xp GIF'
images = []
for filename in filenames_x_xp:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_x_xp/x_xp.gif', images)	

print 'Creating y - yp GIF'
images = []
for filename in filenames_y_yp:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_y_yp/y_yp.gif', images)	

print '\nAll Done! Peace out'
