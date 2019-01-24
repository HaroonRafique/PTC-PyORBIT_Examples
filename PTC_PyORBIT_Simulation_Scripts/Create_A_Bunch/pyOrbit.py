# This example shows us how to create a lattice in PyORBIT using the
# provided MAD-X and PTC scripts

import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import scipy.io as sio
import os

# Use switches in simulation_parameters.py in current folder
#-------------------------------------------------------------
from simulation_parameters import switches as s

# utils
from orbit.utils.orbit_mpi_utils import bunch_orbit_to_pyorbit, bunch_pyorbit_to_orbit
from orbit.utils.consts import mass_proton, speed_of_light, pi

# bunch
from bunch import Bunch
from bunch import BunchTwissAnalysis, BunchTuneAnalysis
from orbit.bunch_utils import ParticleIdNumber

# diagnostics
from orbit.diagnostics import TeapotStatLatsNode, TeapotMomentsNode, TeapotTuneAnalysisNode
from orbit.diagnostics import addTeapotDiagnosticsNodeAsChild
from orbit.diagnostics import addTeapotMomentsNodeSet, addTeapotStatLatsNodeSet

# PTC lattice
from libptc_orbit import *
from ext.ptc_orbit import PTC_Lattice
from ext.ptc_orbit import PTC_Node
from ext.ptc_orbit.ptc_orbit import setBunchParamsPTC, readAccelTablePTC, readScriptPTC
from ext.ptc_orbit.ptc_orbit import updateParamsPTC, synchronousSetPTC, synchronousAfterPTC
from ext.ptc_orbit.ptc_orbit import trackBunchThroughLatticePTC, trackBunchInRangePTC
from orbit.aperture import TeapotApertureNode

from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution2 import *
from lib.save_bunch_as_matfile import *

# MPI initialisation
#-----------------------------------------------------------------------
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)
print '\nPyORBIT: Start on MPI process: ', rank

# Create folder structure
#-----------------------------------------------------------------------
print '\nPyORBIT: mkdir on MPI process: ', rank
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('bunch_output')
mpi_mkdir_p('output')

# Dictionary for simulation status
#-----------------------------------------------------------------------
import pickle # HAVE TO CLEAN THIS FILE BEFORE RUNNING A NEW SIMULATION
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
        sts = {'turn': -1}
else:
        with open(status_file) as fid:
                sts = pickle.load(fid)

# Generate Lattice (MADX + PTC) - Use MPI to run on only one 'process'
#-----------------------------------------------------------------------
print '\nPyORBIT: Start MADX on MPI process: ', rank
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
orbit_mpi.MPI_Barrier(comm)

# Generate PTC RF table
#-----------------------------------------------------------------------
print '\nPyORBIT: start RF file on MPI process: ', rank
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF 
write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])

# Initialize a Teapot-Style PTC lattice
#-----------------------------------------------------------------------
print '\nPyORBIT: start PTC Flat file on MPI process: ', rank
PTC_File = 'PTC-PyORBIT_flat_file.flt'
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

readScriptPTC('Input/fringe.ptc')
readScriptPTC('Input/time.ptc')
readScriptPTC('Input/ramp_cavities.ptc')

# Create a dictionary of parameters
#-----------------------------------------------------------------------
print '\nPyORBIT: paramsDict on MPI process: ', rank
paramsDict = {}
paramsDict["length"] = Lattice.getLength()/Lattice.nHarm

# Add apertures
#-----------------------------------------------------------------------
print '\nPyORBIT: Add apertures on MPI process: ', rank
position = 0
for node in Lattice.getNodes():
	# This creates an aperture node. Shape: 1 = circle, 2 = ellipse,
	# 3 = rectangle. a is the first dimension, either the radius for a 
	# circle, or the half length in the x diminsion. b is the y half 
	# length of the aperture and does nothing for a circle.  c is the x 
	# offset and d is the y offset of the aperture.
	# TeapotApertureNode(self, shape, a, b, pos = 0, c = 0, d = 0, name = "aperture"):
	
	myaperturenode = TeapotApertureNode(1, 10, 10, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()

# Make a bunch and import relevant parameters for it
#-----------------------------------------------------------------------
if sts['turn'] < 0:
	print '\nPyORBIT: Bunches on MPI process: ', rank
	bunch = Bunch()
	setBunchParamsPTC(bunch)

	from simulation_parameters import parameters as p
	p['harmonic_number'] = Lattice.nHarm 
	p['phi_s']           = 0
	p['gamma']           = bunch.getSyncParticle().gamma()
	p['beta']            = bunch.getSyncParticle().beta()
	p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
	p['bunch_length'] = p['blength_rms']/speed_of_light/bunch.getSyncParticle().beta()*4
	kin_Energy = bunch.getSyncParticle().kinEnergy()

	print '\nPyORBIT: bunch_orbit_to_pyorbit on MPI process: ', rank
	for i in p: print '\t', i, '\t = \t', p[i]

# Create the initial distribution 
# Here we have a choice. The current supported options are:
# -Matched distribution using lattice parameters etc
# -Matched distribution with longitudinal part from tomoscope measurement
# -3D Gaussian using lattice parameters
# -Poincare distribution (used for verifying particle motion etc)
# To choose which distribution to use, please change the int distn_type 
# value in ./simulation_parameters.py to one of the following options:
#-----------------------------------------------------------------------
	print '\nPyORBIT: generate_initial_distribution on MPI process: ', rank
	
	if p['distn_type'] == 0:
		print '\nPyORBIT: Generate initial distribution: 3D Gaussian chosen'
		Particle_distribution = generate_initial_distribution_3DGaussian(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
	elif p['distn_type'] == 1:
		print '\nPyORBIT: Generate initial distribution: Distribution from Tomo chosen'
		Particle_distribution = generate_initial_distribution_from_tomo(p, 1, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
	elif p['distn_type'] == 2:
		print '\nPyORBIT: Generate initial distribution: Matched chosen'
		Particle_distribution = generate_initial_distribution(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
	else:
		print '\nPyORBIT: ERROR: Generate initial distribution: \'dist_type\' integer in \'simulation_parameters.py\' set to invalid value. Exiting'
		print (exit)	

	print '\nPyORBIT: \bunch_orbit_to_pyorbit on MPI process: ', rank
	bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
	
# Add Macrosize to bunch
#-----------------------------------------------------------------------
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs

# Dump and save as Matfile
#-----------------------------------------------------------------------
	bunch.dumpBunch("input/mainbunch_start.dat")
	print '\nPyORBIT: Initial bunch dumped to .dat file input/mainbunch_start.dat'
	saveBunchAsMatfile(bunch, "bunch_output/mainbunch_-000001")
	print '\nPyORBIT: Initial bunch dumped to .mat file bunch_output/mainbunch_-000001'
	saveBunchAsMatfile(bunch, "input/mainbunch")
	sts['mainbunch_file'] = "input/mainbunch"
	
# Create empty lost bunch
#-----------------------------------------------------------------------
	lostbunch = Bunch()
	bunch.copyEmptyBunchTo(lostbunch)
	lostbunch.addPartAttr('ParticlePhaseAttributes')
	lostbunch.addPartAttr("LostParticleAttributes")	
	saveBunchAsMatfile(lostbunch, "input/lostbunch")
	sts['lostbunch_file'] = "input/lostbunch"

# Add items to pickle parameters
#-----------------------------------------------------------------------
	sts['turns_max'] = p['turns_max']
	sts['turns_update'] = p['turns_update']
	sts['turns_print'] = p['turns_print']
	sts['circumference'] = p['circumference']

bunch = bunch_from_matfile(sts['mainbunch_file'])
lostbunch = bunch_from_matfile(sts['lostbunch_file'])
paramsDict["lostbunch"] = lostbunch
paramsDict["bunch"] = bunch

# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")

tunes.assignTwiss(*[Twiss_at_parentnode_entrance[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

# Define twiss analysis and output dictionary
#-----------------------------------------------------------------------
print '\nPyORBIT: TWISS on MPI process: ', rank
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

output_file = 'output/output.mat'
output = Output_dictionary()
output.addParameter('turn', lambda: turn)
output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))

if os.path.exists(output_file):
	output.import_from_matfile(output_file)

# Track
#-----------------------------------------------------------------------
print '\nPyORBIT: Tracking on MPI process: ', rank
start_time = time.time()
last_time = time.time()

for turn in range(sts['turn']+1, sts['turns_max']):
	if not rank:
		last_time = time.time()
	if turn == 0:		
		output.addParameter('turn_time', lambda: time.strftime("%H:%M:%S"))
		output.addParameter('turn_duration', lambda: (time.time() - last_time))
		output.addParameter('cumulative_time', lambda: (time.time() - start_time))
		start_time = time.time()
		print 'start time = ', start_time
		
	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
	
	if turn in sts['turns_update']:
		sts['turn'] = turn

	output.update()
	
	if turn in sts['turns_print']:
		saveBunchAsMatfile(bunch, "input/mainbunch")
		saveBunchAsMatfile(bunch, "bunch_output/mainbunch_%s"%(str(turn).zfill(6)))
		output.save_to_matfile(output_file)		        
		if not rank:
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)
