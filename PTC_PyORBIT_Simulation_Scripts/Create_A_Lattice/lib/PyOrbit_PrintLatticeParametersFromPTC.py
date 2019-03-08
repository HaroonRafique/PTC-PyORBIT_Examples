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
	savename = str('PTC_Lattice_Parameters_turn_' + str(turn) + '.dat')
	
	f = open(savename,"w+")
	f.write('# s\tbeta_x\tbeta_y\talpha_x\talpha_y\teta_x\teta_y\teta_px\teta_py\torbit_x\torbit_px\torbit_y\torbit_py')
	
	for i in range(len(s)):
		f.write('\n')
		f.write(str(s[i]))
		f.write('\t')
		f.write(str(beta_x[i]))
		f.write('\t')
		f.write(str(beta_y[i]))
		f.write('\t')
		f.write(str(alpha_x[i]))
		f.write('\t')
		f.write(str(alpha_y[i]))
		f.write('\t')
		f.write(str(eta_x[i]))
		f.write('\t')
		f.write(str(eta_y[i]))
		f.write('\t')
		f.write(str(eta_px[i]))
		f.write('\t')
		f.write(str(eta_py[i]))
		f.write('\t')
		f.write(str(orbit_x[i]))
		f.write('\t')
		f.write(str(orbit_px[i]))
		f.write('\t')
		f.write(str(orbit_y[i]))
		f.write('\t')
		f.write(str(orbit_py[i]))
	
	return
