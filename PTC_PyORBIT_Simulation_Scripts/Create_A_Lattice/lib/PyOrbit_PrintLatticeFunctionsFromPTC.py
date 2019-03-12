#-----------------------------------------------------------------------
# Function to generate output file with PTC lattice parameters
# 08.03.2019: Created by Haroon Rafique, CERN BE-ABP-HSI 
#-----------------------------------------------------------------------
from ext.ptc_orbit import PTC_Lattice
import numpy as np

def PrintLatticeFunctions(Lattice, turn=None, lattice_folder='.'):
		
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
	
	if turn is None:
		savename = str(lattice_folder + '/PTC_Lattice_Parameter.dat')
	else:
		savename = str(lattice_folder + '/PTC_Lattice_Parameters_turn_' + str(turn) + '.dat')
	
	f = open(savename,"w+")
	f.write('# s\tbeta_x\tbeta_y\talpha_x\talpha_y\tD_x\tD_y\tD_px\tD_py\torbit_x\torbit_px\torbit_y\torbit_py')
	
	beta_x = np.array(beta_x)
	beta_y = np.array(beta_y)
	alpha_x = np.array(alpha_x)
	alpha_y = np.array(alpha_y)
	eta_x = np.array(eta_x)
	eta_y = np.array(eta_y)
	eta_px = np.array(eta_px)
	eta_py = np.array(eta_py)
	orbit_x = np.array(orbit_x)
	orbit_px = np.array(orbit_px)
	orbit_y = np.array(orbit_y)
	orbit_py = np.array(orbit_py)
		
	for i in range(0, len(s), 1):
		# ~ print i 
		f.write('\n')
		f.write(str(s[i]))
		f.write('\t')
		f.write(str(beta_x[0][i]))
		f.write('\t')
		f.write(str(beta_y[0][i]))
		f.write('\t')
		f.write(str(alpha_x[0][i]))
		f.write('\t')
		f.write(str(alpha_y[0][i]))
		f.write('\t')
		f.write(str(eta_x[0][i]))
		f.write('\t')
		f.write(str(eta_y[0][i]))
		f.write('\t')
		f.write(str(eta_px[0][i]))
		f.write('\t')
		f.write(str(eta_py[0][i]))
		f.write('\t')
		f.write(str(orbit_x[0][i]))
		f.write('\t')
		f.write(str(orbit_px[0][i]))
		f.write('\t')
		f.write(str(orbit_y[0][i]))
		f.write('\t')
		f.write(str(orbit_py[0][i]))
	
	return
