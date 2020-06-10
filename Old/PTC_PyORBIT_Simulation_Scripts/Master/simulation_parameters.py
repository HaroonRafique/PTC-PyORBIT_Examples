import numpy as np

tomo_file = 'Input/PyORBIT_Tomo_file.mat'

# PS Injection 1.4 GeV
gamma = 2.49253731343
beta = np.sqrt(gamma**2-1)/gamma
c = 299792458

# Beam Parameters
intensity = 7.5e+11
epsn_x = 2.036e-6
epsn_y = 2.225e-6

blength = 210e-9
sig_z = (beta * c * blength)/4.
dpp_rms = 9.81e-04
rf_voltage = 0.0123212966992E6

# Simulation Parameters
n_macroparticles = int(1E3)
turns_max = int(1E1)	
turns_update = range(-1, turns_max, 100)
turns_print =  range(-1, turns_max, 100)
macrosize = intensity/float(n_macroparticles)

# Space Charge
grid_x = 32
grid_y = 32
grid_z = 32

# PTC RF Table Parameters
harmonic_factors = [1] # this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
time = np.array([0,1,2])
ones = np.ones_like(time)
Ekin_GeV = 1.4*ones
RF_voltage_MV = np.array([0.0123212966992*ones]).T # in MV
RF_phase = np.array([np.pi*ones]).T

# Constants
circumference = 2*np.pi*100
m = 1.2					# Longitudinal Joho Parameter
TransverseCut = 5		# Used for some distributions (matched)

parameters = {
	'intensity': intensity,
	'gamma': gamma,
	'bunch_length': blength,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'dpp_rms': dpp_rms,
	'tomo_file': tomo_file,
	'LongitudinalJohoParameter': m,
	'LongitudinalCut': 2.4,
	'n_macroparticles': n_macroparticles,
	'TransverseCut': TransverseCut,
	'macrosize': macrosize,
	'turns_max': turns_max,
	'turns_update': turns_update,
	'turns_print': turns_print,
	'rf_voltage': rf_voltage,
	'circumference':circumference
}

tunespread = {
	'intensity': intensity,
	'gamma': gamma,
	'sig_z': sig_z,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'dpp_rms': dpp_rms,
}

switches = {
	'Horizontal': 1,
	'ImportFromTomo': 1,
	'SliceBySlice': 1,
	'Frozen': 0,
	'GridSizeX': grid_x,
	'GridSizeY': grid_y,
	'GridSizeZ': grid_z
}

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
