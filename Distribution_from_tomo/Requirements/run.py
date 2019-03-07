'''
This script takes an output from the tomo (.dat format), and runs
the file through the executable tomo_vo.intelmp, thus generating a 
.mat file to be read by a PyORBIT distribution generator (written by
CERN BE-ABP-HSI members) which generates the longitudinal distribution
based on the measured tomo data.

This script is based on the work of:
Simon Albright (BE-RF)
Andrea Santamaria Garcia (BE-OP)
Eirini Koukovini-Platia (BE-ABP-HSC)

and is made available by Haroon Rafique (CERN BE-ABP-HSI) as is.
'''

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
from scipy.io import savemat
import sys

# tomo dat file name
input_file_name='C200_001_001_001.dat'
input_file_path=str('./'+input_file_name)

# Run the executable using the input file
result = subprocess.Popen(['./tomo_vo.intelmp'], stdin=open(input_file_path, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()
out = out.splitlines()

# Read created image data, note that the image may be named image002.data
dat = np.loadtxt("image001.data")

# reshape from one column to a square
var = (int(np.sqrt(dat.shape[0])), int(np.sqrt(dat.shape[0])))
dat = dat.reshape(var).T

# format output (out) binsizes
regexp = re.compile("\\d+\\.?\\d*E?[-+]?\\d*")

print(out[7])
print(out[9])

# output data looks like this:
# dtbin = 2.5000E-09
# dEbin = 9.6494E+04

# Save in units of nanoseconds and mega electron volts
dt = float(regexp.findall(out[7])[0])/1E-9 # ns
dE = float(regexp.findall(out[9])[0])/1E6  # MeV
 
# make bins
tAxis = np.arange(dat.shape[0])*dt
EAxis = np.arange(dat.shape[0])*dE

# centre on (0,0) - not exact centre
tAxis -= np.mean(tAxis)
EAxis -= np.mean(EAxis)

# The user must manually check and adjust the bunch centre like this:
# ~ tAxis -= 5									
# ~ EAxis -= .05						

# Set limit for pixels to keep - this can be adjusted empirically
limit = 4E-5		

for x,y in np.ndindex(dat.shape):
	if dat[x,y] < limit:					
		dat[x,y] = 0.0	
		
# This filters any pixel where surrounding pixels are 0
# may need to be modified if your phase space isn't a bunch but
# contains some sort of lines / filamentation that is wanted
for x in range (0, dat.shape[0], 1):
	for y in range( 0, dat.shape[1], 1):
		if x == 0 or y == 0 or x == (dat.shape[0]-1) or y == (dat.shape[1]-1) or dat[x,y] == 0.0:
			pass
		else: 
			if dat[x, y-1] == 0.0 and dat[x, y+1] == 0.0:
				print 'outlier removed at [',x, ',' ,y, ']'
				dat[x,y] = 0.0			

# access outliers manually like this
# dat[65, 3]    =  0.0
# dat[67, 127]  =  0.0
# dat[82, 112]  =  0.0

# plot for inspection
fig, ax = plt.subplots()
ax.pcolor(tAxis, EAxis, dat)
ax.set(xlabel='dt [ns]', ylabel='dE [MeV]', title='Longitudinal distribution from tomo data')
ax.grid(True)
plot_name = input_file_name + '.png'
fig.savefig(plot_name, dpi=600)

# Save file for PyORBIT
data_dict = {'time_nsec': tAxis, 'energy_MeV': EAxis, 'density_array': dat}
savemat('PyORBIT_Tomo_file.mat', data_dict)
