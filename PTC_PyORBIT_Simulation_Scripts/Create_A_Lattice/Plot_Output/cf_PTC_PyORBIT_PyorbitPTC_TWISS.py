# Plot Courant-Snyder parameters calculated in PTC and PyORBIT to 
# compare

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5

# Open Files

ptc_file='../ptc_twiss'
pyorbit_file='../output/StatLats.dat'
ptc_from_pyorbit_file = '../lattice/PTC_Lattice_Parameters_turn_-1.dat'

fin1=open(pyorbit_file,'r').readlines()[8:]
# ~ firstLine = fin1.pop(8)

s_po_ptc = []
betx_po_ptc = []
bety_po_ptc = []
alfx_po_ptc = []
alfy_po_ptc = []
dx_po_ptc = []

s_po = []
betx_po = []
bety_po = []
alfx_po = []
alfy_po = []
dx_po = []

s = []
betx = []
bety = []
alfx = []
alfy = [] 
dx = []
dy = []

beta = 0.915961016423
gamma =	2.49210461976

print 'Reading PTC twiss file'
# Read Data
for l in fin1:
	# (1) azimuthal position around ring, s [m]
	# (2) time
	# (3) emittance_x
	# (4) emittance_y
	# (5) beta_x [m]
	# (6) beta_y [m]
	# (7) alpha_x
	# (8) alpha_y
	# (9) D_x [m]
	# (10) dD_x
    s_po.append(float(l.split()[0]))
    betx_po.append(float(l.split()[4]))
    bety_po.append(float(l.split()[5]))
    alfx_po.append(float(l.split()[6]))
    alfy_po.append(float(l.split()[7]))    
    dx_po.append(float(l.split()[8]))
    

print 'Reading PyORBIT lattice file'
# Skip header
fin2=open(ptc_file,'r').readlines()[90:]

for f in fin2:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    s.append(float(f.split()[1]))
    betx.append(float(f.split()[2]))
    bety.append(float(f.split()[3]))
    alfx.append(float(f.split()[4]))
    alfy.append(float(f.split()[5]))
    dx.append(float(f.split()[6]) * beta)
    dy.append(float(f.split()[7]) * beta)
    

print 'Reading PTC from PyORBIT twiss file'
# Skip header
fin3=open(ptc_from_pyorbit_file,'r').readlines()[1:]

for f in fin3:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    s_po_ptc.append(float(f.split()[0]))
    betx_po_ptc.append(float(f.split()[1]))
    bety_po_ptc.append(float(f.split()[2]))
    alfx_po_ptc.append(float(f.split()[3]))
    alfy_po_ptc.append(float(f.split()[4]))
    dx_po_ptc.append(float(f.split()[5]))

#############
#   Beta x  #
#############
print 'Plotting beta_x'
fig, ax1 = plt.subplots();

plt.title("PTC vs PyORBIT Beta x");

ax1.plot(s, betx, 'k', label=r'PTC $\beta_x$', linewidth=1);
ax1.scatter(s_po, betx_po, color='b', marker ='d', label=r'PyORBIT $\beta_x$');
ax1.scatter(s_po_ptc, betx_po_ptc, color='r', marker ='d',  label=r'PTC from PyORBIT $\beta_x$');

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\beta_x$ [m]", color='b');

# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

#ax1.set_ylim(0,100)
ax1.set_xlim(0,100)

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Beta_x_.png', dpi = 800);

#############
#   Beta x  #
#############
print 'Plotting beta_x'
fig, ax1 = plt.subplots();

plt.title("PTC vs PyORBIT Beta x");

ax1.plot(s, betx, 'k', label=r'PTC $\beta_x$', linewidth=1);
ax1.scatter(s_po, betx_po, color='b', marker='d', label=r'PyORBIT $\beta_x$', linewidth=1);
ax1.scatter(s_po_ptc, betx_po_ptc, color='r', marker='d', label=r'PTC from PyORBIT $\beta_x$', linewidth=1);

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\beta_x$ [m]", color='b');

# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

#ax1.set_ylim(0,100)

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Beta_x.png', dpi = 800);
    
#############
#   Beta y  #
#############
print 'Plotting beta_y'
fig, ax1 = plt.subplots();

plt.title("PTC vs PyORBIT Beta y");

ax1.plot(s, bety, 'k', label=r'PTC $\beta_y$', linewidth=1);
ax1.scatter(s_po, bety_po, color='b', marker='d', label=r'PyORBIT $\beta_y$', linewidth=1);
ax1.scatter(s_po_ptc, bety_po_ptc, color='r', marker='d', label=r'PTC from PyORBIT $\beta_y$', linewidth=1);

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\beta_y$ [m]", color='b');

# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

#ax1.set_ylim(0,100)

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Beta_y.png', dpi = 800);
    
        
##############
#   Alpha x  #
##############
print 'Plotting alpha_x'
fig, ax1 = plt.subplots();

plt.title(r"PTC vs PyORBIT $\alpha_x$");

ax1.plot(s, alfx, 'k', label=r'PTC $\alpha_x$', linewidth=1);
ax1.scatter(s_po, alfx_po, color='b', marker='d', label=r'PyORBIT $\alpha_x$', linewidth=1);
ax1.scatter(s_po_ptc, alfx_po_ptc, color='r', marker='d', label=r'PTC from PyORBIT $\alpha_x$', linewidth=1);

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\alpha_x$ [-]", color='b');

# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Alpha_x.png', dpi = 800);

##############
#   Alpha y  #
##############
print 'Plotting alpha_y'
fig, ax1 = plt.subplots();

plt.title(r"PTC vs PyORBIT $\alpha_y$");

ax1.plot(s, alfy, 'k', label=r'PTC $\alpha_y$', linewidth=1);
ax1.scatter(s_po, alfy_po, color='b', marker='d', label=r'PyORBIT $\alpha_y$', linewidth=1);
ax1.scatter(s_po_ptc, alfy_po_ptc, color='r', marker='d', label=r'PTC from PyORBIT $\alpha_y$', linewidth=1);

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\alpha_y$ [-]", color='b');

# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Alpha_y.png', dpi = 800);


#################
#   Dispersion  #
#################
print 'Plotting D_x'
fig, ax1 = plt.subplots();

plt.title("PTC Dispersion Functions");
ax1.plot(s, dx, 'k', label=r'PTC $D_x$', linewidth=1);
ax1.scatter(s_po, dx_po, color='b', marker='d', label=r'PyORBIT $D_x$', linewidth=1);
ax1.scatter(s_po_ptc, dx_po_ptc, color='r', marker='d', label=r'PTC from PyORBIT $D_x$', linewidth=1);

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$D_x$ [m]", color='b');

ax1.tick_params('y', colors='b');

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax2 = ax1.twinx();
ax2.plot(s, dy, 'r:', label=r'PTC $D_y$', linewidth=1);
ax2.set_ylabel(r"$D_y$ [m]", color='r');
ax2.tick_params('y', colors='r');

ax1.legend(loc = 2);
ax2.legend(loc = 1);

#fig.tight_layout();
plt.savefig('Dispersion_functions.png', dpi = 800);
