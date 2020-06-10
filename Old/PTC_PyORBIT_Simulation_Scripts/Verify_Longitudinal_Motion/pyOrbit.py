import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import scipy.io as sio
import os

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

# CERN libs
from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution import *
from lib.pyOrbit_ParticleOutputDictionary import *
from lib.save_bunch_as_matfile import *
from lib.suppress_stdout import suppress_STDOUT
readScriptPTC_noSTDOUT = suppress_STDOUT(readScriptPTC)


# MPI stuff
#-----------------------------------------------------------------------
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)
print 'Start on MPI process: ', rank


# Create folder structure
#-----------------------------------------------------------------------
print '\nmkdir on MPI process: ', rank
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('bunch_output')
mpi_mkdir_p('output')
mpi_mkdir_p('lost')


# Dictionary for simulation status
#-----------------------------------------------------------------------
import pickle # HAVE TO CLEAN THIS FILE BEFORE RUNNING A NEW SIMULATION
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
        sts = {'turn': -1}
else:
        with open(status_file) as fid:
                sts = pickle.load(fid)


# Generate PTC RF table
#-----------------------------------------------------------------------
print '\nstart RF file on MPI process: ', rank
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF 
write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])


# Initialize a Teapot-Style PTC lattice
#-----------------------------------------------------------------------
print '\nstart PTC Flat file on MPI process: ', rank
PTC_File = "Lattice/PTC-PyORBIT_flat_file.flt"
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

readScriptPTC_noSTDOUT('PTC/fringe.ptc')
readScriptPTC_noSTDOUT('PTC/time.ptc')
readScriptPTC_noSTDOUT('PTC/ramp_cavities.ptc')


# Create a dictionary of parameters
#-----------------------------------------------------------------------
print '\nparamsDict on MPI process: ', rank
paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm


# Add apertures
#-----------------------------------------------------------------------
print '\nAdd apertures on MPI process: ', rank
position = 0
for node in Lattice.getNodes():
	myaperturenode = TeapotApertureNode(1, 10, 10, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()


# Make a bunch and import relevant parameters for it
#-----------------------------------------------------------------------
if sts['turn'] < 0:
	print '\nBunches on MPI process: ', rank
	bunch = Bunch()
	setBunchParamsPTC(bunch)

	from simulation_parameters import parameters as p
	p['harmonic_number'] = Lattice.nHarm 
	p['phi_s']           = 0
	p['gamma']           = bunch.getSyncParticle().gamma()
	p['beta']            = bunch.getSyncParticle().beta()
	p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
	p['bunch_length'] = p['bunch_length']
	kin_Energy = bunch.getSyncParticle().kinEnergy()

	print '\nbunch_orbit_to_pyorbit on MPI process: ', rank
	for i in p:
		print '\t', i, '\t = \t', p[i]


# Create the initial distribution 
#-----------------------------------------------------------------------
	print '\ngenerate_initial_distribution on MPI process: ', rank
	z_init = 0.5
	Particle_distribution = generate_initial_long_poincare_distribution(z_init, p, Lattice, zero_particle=True, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

	print '\bunch_orbit_to_pyorbit on MPI process: ', rank
	bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
	
	
# Add Macrosize to bunch
#-----------------------------------------------------------------------
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs


# Dump and save as Matfile
#-----------------------------------------------------------------------
	bunch.dumpBunch("input/mainbunch_start.dat")
	saveBunchAsMatfile(bunch, "bunch_output/mainbunch_-000001")
	saveBunchAsMatfile(bunch, "input/mainbunch")
	sts['mainbunch_file'] = "input/mainbunch.mat"
	bunch = bunch_from_matfile(sts['mainbunch_file'])


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
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch


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
print '\nTWISS on MPI process: ', rank
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

if os.path.exists(output_file):	output.import_from_matfile(output_file)	
	
	
# Define particle output dictionary - automatically adds first particle
#-----------------------------------------------------------------------
particle_output = Particle_output_dictionary()


# Track
#-----------------------------------------------------------------------
print '\nTracking on MPI process: ', rank
start_time = time.time()
last_time = time.time()

for turn in range(sts['turn']+1, sts['turns_max']):
	if not rank:	last_time = time.time()
	
	if turn == 0:		
		output.addParameter('turn_time', lambda: time.strftime("%H:%M:%S"))
		output.addParameter('turn_duration', lambda: (time.time() - last_time))
		output.addParameter('cumulative_time', lambda: (time.time() - start_time))
		start_time = time.time()
		print 'start time = ', start_time
		
	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
					
	if turn in sts['turns_update']:	sts['turn'] = turn

	output.update()
	particle_output.Update(bunch, turn)
	
	if turn in sts['turns_print']:
		saveBunchAsMatfile(bunch, "input/mainbunch")
		saveBunchAsMatfile(bunch, "bunch_output/mainbunch_%s"%(str(turn).zfill(6)))
		saveBunchAsMatfile(lostbunch, "lost/lostbunch_%s"%(str(turn).zfill(6)))
		output.save_to_matfile(output_file)		        
		if not rank:
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)
				
particle_output.PrintParticle(0)		

# Need number of turns to return to starting position. Let's read the
# particle output file
#-----------------------------------------------------------------------

print '\n\tReading particle dictionary'

z=[]

filename='Particle_0.dat'
fin=open(filename,'r').readlines()[1:]

for l in fin:
	z.append(float(l.split()[6]))
	
print '\n\tz_0 from simulation = ', z_init
print '\n\tz_0 from file (actual value) = ', z[0]

# Now iterate over z position to find full oscillation
tolerance = 1E-4

print '\n\tTolerance for finding full oscillation = ', tolerance

for i in xrange(len(z)): 
	if (abs(z[i] - z[0]) < tolerance): synch_turns = i
		
print '\n\tSynchrotron period in turns = ', synch_turns

# We know our expected synchrotron oscillation period:
synch_oscillation_period = 634 #Hz

calculated_synch_oscillation_period = 1 /( (synch_turns * p['circumference']) / (p['beta'] * speed_of_light) )

print '\n\tExpected Synchrotron Period = ', synch_oscillation_period, ' Hz'
print '\n\tCalculated Synchrotron Period = ', calculated_synch_oscillation_period, ' Hz'

print '\n\tDifference in Synchrotron Periods =', abs(synch_oscillation_period - calculated_synch_oscillation_period), 'Hz'

print '\n\tDifference in Synchrotron Periods =', (abs(synch_oscillation_period - calculated_synch_oscillation_period)/ synch_oscillation_period)*100, '%'

print '\n\tLongitudinal Test Simulation Finished! Have an awesome day :-)'
