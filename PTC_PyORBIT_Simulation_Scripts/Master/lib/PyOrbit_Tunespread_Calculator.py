#-----------------------------------------------------------------------
# Function to calculate tunespread from bunch parameters
# Uses Adrian Oeftiger's (CERN BE-ABP-HSC) tunespread calculator
# 12.03.2019: Created by Haroon Rafique, CERN BE-ABP-HSI 
# Required parameters:
# particle mass in GeV (provided)
# Lorentz gamma and beta
# sig_z or bunch length
# number of particles
# normalised or geometrical horizontal emittance 
#		e_norm = e_geom * beta * gamma
# normalised or geometrical vertical emittance
# delta_p/p
# charge per particle
# lineshape (for multiple harmonics, default = 1)
#-----------------------------------------------------------------------
from spacecharge_tunespread.tunespread import *
from scipy import constants as const

def TunespreadCalculator(parameters, twissfile='ptc_twiss')	
	
	# Default particle is proton
	print 'PyOrbit_Tunespread_Calculator: Assuming particle is a proton. Please change mass if not the case'
	mass = mp # = 0.938272046 Proton mass in GeV
	# ~ mass = me # 0.510998928e-3 # electron mass in GeV
	
	if 'gamma' in parameters:
		gamma = parameters['gamma']
	elif 'E_kin' in parameters:
		gamma = parameters["E_kin"] / mass + 1.0
		
	beta = np.sqrt(gamma**2-1)/gamma
		
	if 'bunch_length_rms' in parameters:
		sig_z = ( 1.0e-9 * beta * const.c * parameters["bunch_length_rms"] / 4.0 )
	elif 'sig_z' in parameters:
		sig_z = parameters['sig_z']
		
	n_part = parameters['n_macroparticles']
	
	if 'epsn_x' in parameters:	epsn_x = parameters['epsn_x']
	if 'epsn_y' in parameters:	epsn_y = parameters['epsn_y']

	if 'dpp_rms' in parameters: deltap = parameters['dpp_rms']
		
	params = {'n_part': n_part, 'emit_norm_x': emit_x, 'emit_norm_y': emit_y, 'gamma': gamma, 'deltap': deltap, 'n_charges_per_part': 1, 'lshape': 1., 'sig_z': sig_z, 'coasting': False} 
	
	data, inputs = ext.get_inputs(twissfile, params, False, False)
	dQ = calc_tune_spread(data, inputs)
	print inputs
	ext.print_verbose_output(inputs, data, dQ[0], dQ[1])
	print "dQx = %2.3f, dQy = %2.3f"%(dQ[0], dQ[1])
	
	return
