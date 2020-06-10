import orbit_mpi
from orbit_mpi import mpi_datatype
from orbit_mpi import mpi_op
import numpy as np
import scipy.io as sio
from bunch import Bunch

# 12.03.2017: works now also for lostbunch attributes
# 03.06.2017: now a bunch object can be generated from a matfile
# 17.02.2018: now a bunch object can be generated from a matfile even if it contains only a single particle

def saveBunchAsMatfile(bunch, filename=None):

	b = bunch
	#take the MPI Communicator from bunch: it could be different from MPI_COMM_WORLD
	comm = b.getMPIComm()
	rank = orbit_mpi.MPI_Comm_rank(comm)
	size = orbit_mpi.MPI_Comm_size(comm)	
	main_rank = 0

	# n_parts_arr - array of size of the number of CPUs, 
	# and have the number of macroparticles on each CPU
	n_parts_arr = [0]*size
	n_parts_arr[rank] = b.getSize()
	n_parts_arr = orbit_mpi.MPI_Allreduce(n_parts_arr,mpi_datatype.MPI_INT,mpi_op.MPI_SUM,comm)	

	mp_array = range(n_parts_arr[rank])
	particles = {}
	particles['x'] = map(b.x, mp_array)
	particles['xp'] = map(b.xp, mp_array)
	particles['y'] = map(b.y, mp_array)
	particles['yp'] = map(b.yp, mp_array)
	particles['z'] = map(b.z, mp_array)
	particles['dE'] = map(b.dE, mp_array)
	phase_space_keys = particles.keys()

	for attribute in b.getPartAttrNames():
		particles[attribute] = [[] for i in range(b.getPartAttrSize(attribute))]
		for j in xrange(b.getPartAttrSize(attribute)):
			particles[attribute][j] += map(lambda i: b.partAttrValue(attribute, i, j), mp_array)

	#This is just for case. Actually, MPI_Barrier command is not necessary.
	orbit_mpi.MPI_Barrier(comm)

	for i_cpu in range(1,size):
		for key in phase_space_keys:
			if(rank == main_rank):
				#get the particle coordinates and attributes
				bunch_size_remote = orbit_mpi.MPI_Recv(mpi_datatype.MPI_INT,i_cpu,222,comm)
				if bunch_size_remote:
					particles[key] += list(np.atleast_1d(orbit_mpi.MPI_Recv(mpi_datatype.MPI_DOUBLE,i_cpu,222,comm)))
			elif(rank == i_cpu):
				#send the coordinate array if there are any particles ...
				bunch_size_local = bunch.getSize()
				orbit_mpi.MPI_Send(bunch_size_local,mpi_datatype.MPI_INT,main_rank,222,comm)
				if bunch_size_local:
					orbit_mpi.MPI_Send(particles[key],mpi_datatype.MPI_DOUBLE,main_rank,222,comm)

	for i_cpu in range(1,size):
		for attribute in b.getPartAttrNames():
			if(rank == main_rank):
				bunch_size_remote = orbit_mpi.MPI_Recv(mpi_datatype.MPI_INT,i_cpu,222,comm)
				if bunch_size_remote:
					#get the particle coordinates and attributes
					for j in xrange(b.getPartAttrSize(attribute)):
						particles[attribute][j] += list(np.atleast_1d(orbit_mpi.MPI_Recv(mpi_datatype.MPI_DOUBLE,i_cpu,222,comm)))
			elif(rank == i_cpu):
				bunch_size_local = bunch.getSize()
				orbit_mpi.MPI_Send(bunch_size_local,mpi_datatype.MPI_INT,main_rank,222,comm)
				if bunch_size_local:
					#send the coordinate array if there are any particles ...
					for j in xrange(b.getPartAttrSize(attribute)):
						orbit_mpi.MPI_Send(particles[attribute][j],mpi_datatype.MPI_DOUBLE,main_rank,222,comm)

	bunchparameters = {'classical_radius': bunch.classicalRadius(), \
					   'charge': bunch.charge(), 
					   'mass': bunch.mass(), \
					   'momentum': bunch.getSyncParticle().momentum(), \
					   'beta': bunch.getSyncParticle().beta(), \
					   'gamma': bunch.getSyncParticle().gamma(), \
					   'time': bunch.getSyncParticle().time()}

	if filename:
		if rank == main_rank:
			sio.savemat(filename + '.mat', {'particles': particles, 'bunchparameters': bunchparameters}, do_compression=True)
	orbit_mpi.MPI_Barrier(comm)


def bunch_from_matfile(matfile):
	d = sio.loadmat(matfile, squeeze_me=True)
	p = dict((key, value) for (key, value) in map(lambda k: (k, d['particles'][k][()]), d['particles'].dtype.names))
	attributes = list(set(p) - set(['x', 'xp', 'y', 'yp', 'z', 'dE']))
	attributes.sort(key=str.lower)

	bunch = Bunch()
	bunch.classicalRadius(d['bunchparameters']['classical_radius'])
	bunch.charge(d['bunchparameters']['charge'])
	bunch.mass(d['bunchparameters']['mass'])
	bunch.getSyncParticle().momentum(d['bunchparameters']['momentum'])
	bunch.getSyncParticle().time(d['bunchparameters']['time'])

	x  = np.atleast_1d(d['particles']['x'][()])
	xp = np.atleast_1d(d['particles']['xp'][()])
	y  = np.atleast_1d(d['particles']['y'][()])
	yp = np.atleast_1d(d['particles']['yp'][()])
	z  = np.atleast_1d(d['particles']['z'][()])
	dE = np.atleast_1d(d['particles']['dE'][()])
	n_part = len(x)

	import orbit_mpi
	comm = bunch.getMPIComm()
	rank = orbit_mpi.MPI_Comm_rank(comm)
	size = orbit_mpi.MPI_Comm_size(comm)

	count = n_part / size
	remainder = n_part % size
	if (rank < remainder):
		i_start = rank * (count + 1)
		i_stop = i_start + count+1
	else:
		i_start = rank * count + remainder
		i_stop = i_start + count;
	# print rank, i_start, i_stop

	map(lambda i: bunch.addParticle(x[i],xp[i],y[i],yp[i],z[i],dE[i]), xrange(i_start,i_stop))
	orbit_mpi.MPI_Barrier(comm)
	for a in attributes:
		bunch.addPartAttr(a)
		a_size = bunch.getPartAttrSize(a)
		if a_size>1:
			for j in xrange(a_size):
				map(lambda (ip,i): bunch.partAttrValue(a, ip, j, np.atleast_1d(p[a][j])[i]), enumerate(xrange(i_start,i_stop)))
		else:
			map(lambda (ip,i): bunch.partAttrValue(a, ip, 0, np.atleast_1d(p[a])[i]), enumerate(xrange(i_start,i_stop)))
	orbit_mpi.MPI_Barrier(comm)
	return bunch