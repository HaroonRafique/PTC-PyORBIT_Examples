#-----------------------------------------------------------------------
# Function to generate output file with PTC lattice parameters
# 08.03.2019: Created by Haroon Rafique, CERN BE-ABP-HSI 
#-----------------------------------------------------------------------
from ext.ptc_orbit import PTC_Lattice
import numpy as np

def PrintLatticeParameters(Lattice, turn):
	
	# Empty arrays
	beta_x = []
	beta_y = []
	alpha_x = []
	alpha_y = []
	eta_x = []
	eta_y = []
	eta_px = []
	eta_py = []
	orbit_x = []
	orbit_px = []
	orbit_y = []
	orbit_py = []
	
	beta_x.append([n.getParamsDict()['betax'] for n in Lattice.getNodes()])
	beta_y.append([n.getParamsDict()['betay'] for n in Lattice.getNodes()])
	alpha_x.append([n.getParamsDict()['alphax'] for n in Lattice.getNodes()])
	alpha_y.append([n.getParamsDict()['alphay'] for n in Lattice.getNodes()])
	eta_x.append([n.getParamsDict()['etax'] for n in Lattice.getNodes()])
	eta_y.append([n.getParamsDict()['etay'] for n in Lattice.getNodes()])
	eta_px.append([n.getParamsDict()['etapx'] for n in Lattice.getNodes()])
	eta_py.append([n.getParamsDict()['etapy'] for n in Lattice.getNodes()])
	orbit_x.append([n.getParamsDict()['orbitx'] for n in Lattice.getNodes()])
	orbit_px.append([n.getParamsDict()['orbitpx'] for n in Lattice.getNodes()])
	orbit_y.append([n.getParamsDict()['orbity'] for n in Lattice.getNodes()])
	orbit_py.append([n.getParamsDict()['orbitpy'] for n in Lattice.getNodes()])
	
	s = np.cumsum([n.getLength() for n in Lattice.getNodes()])
	
	np.savetxt('PTC_Lattice_Parameters.dat', (beta_x, beta_y, alpha_x, alpha_y, eta_x, eta_y, eta_px, eta_py, orbit_x, orbit_y, orbit_px, orbit_py))
	
	return
