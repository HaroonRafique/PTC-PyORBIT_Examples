import numpy as np

tomo_file = 'Input/PyORBIT_Tomo_file.mat'

# Beam Parameters
intensity = 2e+12
epsn_x = 2.036e-6
epsn_y = 2.225e-6

blength_rms = (0.91*299792458*210e-9)/4.
dpp_rms = 9.81e-04
rf_voltage = 0.0123212966992E6

# Simulation Parameters
# Noise test
n_macroparticles = int(1E4)
turns_max = int(1E2)	
#turns_max = int(1E4)	
turns_update = range(-1, turns_max, 10)
turns_print =  range(-1, turns_max, 10)

grid_x = 64
grid_y = 64
grid_z = 32

macrosize = intensity/float(n_macroparticles)

# these are the paramters for the PTC RF table
harmonic_factors = [1] #this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
time = np.array([0,1,2])
ones = np.ones_like(time)
Ekin_GeV = 1.4*ones
RF_voltage_MV = np.array([0.0123212966992*ones]).T # in MV
RF_phase = np.array([np.pi*ones]).T

# Constants
circumference = 2*np.pi*100
m = 1.2
TransverseCut = 5

parameters = {
	'tomo_file': tomo_file,
	'LongitudinalJohoParameter': m,
	'LongitudinalCut': 2.4,
	'blength_rms': blength_rms,
	'n_macroparticles': n_macroparticles,
	'intensity': intensity,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'dpp_rms': dpp_rms,
	'TransverseCut': TransverseCut,
	'macrosize': macrosize,
	'turns_max': turns_max,
	'turns_update': turns_update,
	'turns_print': turns_print,
	'rf_voltage': rf_voltage,
	'circumference':circumference
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
