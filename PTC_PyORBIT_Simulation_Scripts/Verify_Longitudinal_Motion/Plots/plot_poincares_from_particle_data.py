# Plots the poincare sections in 5 phase spaces
# x-y x-xp y-yp xp-yp z-dE
# Over many turns.
# Uses all file Particle_0.dat produced using the CERN authored
# particle output dictionary

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 
import os
import sys

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.handlelength'] = 5

plt.rcParams['agg.path.chunksize'] = 1000

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

case = 'CERN_PS_Longitudinal_Check'

# Read file, looks like:
#ParticleID	Turn	x[m]	xp	y[m]	yp	z[m]	dE[GeV]

# Make arrays to hold everything simply - assume only 1 particle here
Pid=[]
Turn=[]
x=[]
xp=[]
y=[]
yp=[]
dE=[]
z=[]
particles=[]

filename='Particle_0.dat'
fin=open(filename,'r').readlines()[1:]

for l in fin:
	
	if int(l.split()[0]) not in Pid:
		particles.append(int(l.split()[0]))
		
	Pid.append(int(l.split()[0]))
	Turn.append(int(l.split()[1]))
	x.append(float(l.split()[2]))
	xp.append(float(l.split()[3]))
	y.append(float(l.split()[4]))
	yp.append(float(l.split()[5]))
	z.append(float(l.split()[6]))
	dE.append(float(l.split()[7]))
	

print 'Number of particles in input file: ', len(particles)
print 'Number of turns in input file: ', max(Turn)+1

if len(particles) > 1:
	print 'Warning: This script is designed to take data from only a single particle'
	
##########
#   z    #
##########
fig, ax1 = plt.subplots();

ax1.scatter(Turn, z, color='m', marker='.');
        
ax1.set_xlabel('Turn [-]');
ax1.set_ylabel('z [m]');
ax1.set_title('Particle z co-ordinate as a function of turn');
ax1.grid(True);


print 'z_0 = ', z[0]
print 'z_f = ', z[-1]

print 'z_f - z_0 = ', (z[-1] - z[0])

savename = 'Particle_motion_z_'+case+'.png'
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);

#####################
#   z dE Poincare   #
#####################
fig, ax1 = plt.subplots();
ax1.scatter(z, dE, color='m', marker='.');

ax1.set_xlabel('z [m]');
ax1.set_ylabel('dE [GeV]');
ax1.set_title('z dE Poincare');
ax1.grid(True);

savename = 'Poincare_z_dE_'+case+'.png'
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);

#####################
#   x xp Poincare   #
#####################
fig, ax1 = plt.subplots();
ax1.scatter(x, xp, color='m', marker='.');

ax1.set_xlabel('x [m]');
ax1.set_ylabel('xp [mrad]');
ax1.set_title('x xp Poincare');
ax1.grid(True);

savename = 'Poincare_x_xp_'+case+'.png'
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);

#####################
#   y yp Poincare   #
#####################
fig, ax1 = plt.subplots();
ax1.scatter(y, yp, color='m');

ax1.set_xlabel('y [m]');
ax1.set_ylabel('yp [mrad]');
ax1.set_title('y yp Poincare');
ax1.grid(True);

savename = 'Poincare_y_yp_'+case+'.png'
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);

#####################
#   x y Poincare   #
#####################
fig, ax1 = plt.subplots();
ax1.scatter(x, y, color='m');

ax1.set_xlabel('x [m]');
ax1.set_ylabel('y [m]');
ax1.set_title('x y Poincare');
ax1.grid(True);

savename = 'Poincare_x_y_'+case+'.png'
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);

#####################
#   xp yp Poincare   #
#####################
fig, ax1 = plt.subplots();
ax1.scatter(xp, yp, color='m');

ax1.set_xlabel('xp [mrad]');
ax1.set_ylabel('yp [mrad]');
ax1.set_title('xp yp Poincare');
ax1.grid(True);

savename = 'Poincare_xp_yp_'+case+'.png'
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);

print '\n\n\nALL DONE! PEACE OUT'
