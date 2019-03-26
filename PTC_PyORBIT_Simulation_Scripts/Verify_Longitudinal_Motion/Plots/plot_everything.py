# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 

# Function takes:
# parameter name; e.g. 'bunch_length'
# title for plot; e.g. 'Bunch Length'
# filename; e.g. 'PS_Injection' = PS_Injection_bunch_length.png
# x and y limits (default is auto)
# Can set y limits individually but not x for some strange reason
# y label; e.g. 'Bunch Length [m]'
# percentage - switch used to plot raw or percentage change from initial value

def plot_parameter(parameter, filename, title=None, ylab=None, yunit='-', ymin=None, ymax=None, percentage = False):

	if percentage:
		print '\nPlotting ', parameter, ' percentage'
	else:
		print '\nPlotting ', parameter

	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = parameter
		
	if title is None:
		title = parameter
		
	if percentage:
		ax1.plot(particles['turn'][0], ((particles[parameter][0]/particles[parameter][0][0])*100)-100, label=parameter);
		ylabel = str(parameter + ' percentage change [%]')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_percentage.png'

	else:
		ax1.plot(particles['turn'][0], particles[parameter][0], label=parameter);
		ylabel = str( parameter + ' [' + yunit + ']')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;
	
	
def plot_mean_of_two_parameters(parameter1, parameter2, filename, title=None, ylab=None, yunit='-', ymin=None, ymax=None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if title is None:
		title = 'mean of ' + parameter1 + ' and ' + parameter2

	ax1.plot(particles['turn'][0], (particles[parameter1][0] + particles[parameter2][0])/2);
	ylabel = str( 'mean of ' + parameter1 + ' and ' + parameter2 + ' [' + yunit + ']')
	ax1.set_ylabel(ylabel);
	figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	ax1.legend()
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;


plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'

plt.rcParams['lines.linewidth'] = 0.5
###########################
# Open file and read data #
###########################

file_in = 'output.mat'
main_label = 'Long Distn Test: Voltage'

particles = dict()
sio.loadmat(file_in, mdict=particles)

# Parameters
# ~ output.addParameter('turn', lambda: turn)
# ~ output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
# ~ output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
# ~ output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
# ~ output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
# ~ output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
# ~ output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
# ~ output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
# ~ output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
# ~ output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
# ~ output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
# ~ output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
# ~ output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
# ~ output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
# ~ output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))

plot_parameter(parameter = 'intensity', filename ='PS_Injection', yunit = 'protons', percentage = False)
plot_parameter(parameter = 'intensity', filename ='PS_Injection', yunit = 'protons', percentage = True)

plot_parameter(parameter = 'mean_x', filename ='PS_Injection', yunit = 'm', percentage = False)
plot_parameter(parameter = 'mean_x', filename ='PS_Injection', yunit = 'm', percentage = True)

plot_parameter(parameter = 'mean_xp', filename ='PS_Injection', yunit = 'rad', percentage = False)
plot_parameter(parameter = 'mean_xp', filename ='PS_Injection', yunit = 'rad', percentage = True)

plot_parameter(parameter = 'mean_y', filename ='PS_Injection', yunit = 'm', percentage = False)
plot_parameter(parameter = 'mean_y', filename ='PS_Injection', yunit = 'm', percentage = True)

plot_parameter(parameter = 'mean_yp', filename ='PS_Injection', yunit = 'rad', percentage = False)
plot_parameter(parameter = 'mean_yp', filename ='PS_Injection', yunit = 'rad', percentage = True)

plot_parameter(parameter = 'mean_z', filename ='PS_Injection', yunit = 'm', percentage = False)
plot_parameter(parameter = 'mean_z', filename ='PS_Injection', yunit = 'm', percentage = True)

plot_parameter(parameter = 'mean_dE', filename ='PS_Injection', yunit = 'GeV', percentage = False)
plot_parameter(parameter = 'mean_dE', filename ='PS_Injection', yunit = 'GeV', percentage = True)

plot_parameter(parameter = 'epsn_x', filename ='PS_Injection', yunit = 'm rad', percentage = False)
plot_parameter(parameter = 'epsn_x', filename ='PS_Injection', yunit = 'm rad', percentage = True)

plot_parameter(parameter = 'epsn_y', filename ='PS_Injection', yunit = 'm rad', percentage = False)
plot_parameter(parameter = 'epsn_y', filename ='PS_Injection', yunit = 'm rad', percentage = True)

plot_parameter(parameter = 'eps_z', filename ='PS_Injection', yunit = 'eV s', percentage = False)
plot_parameter(parameter = 'eps_z', filename ='PS_Injection', yunit = 'eV s', percentage = True)

plot_parameter(parameter = 'bunchlength', filename ='PS_Injection', yunit = 'm', percentage = False)
plot_parameter(parameter = 'bunchlength', filename ='PS_Injection', yunit = 'm', percentage = True)

plot_parameter(parameter = 'dpp_rms', filename ='PS_Injection', yunit = '-', percentage = False)
plot_parameter(parameter = 'dpp_rms', filename ='PS_Injection', yunit = '-', percentage = True)

plot_mean_of_two_parameters(parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename ='PS_Injection', yunit = 'm rad')
