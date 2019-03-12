import orbit_mpi

def only_main_rank(func):
	def call(*args, **kwargs):
		comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
		rank = orbit_mpi.MPI_Comm_rank(comm)
		#print 'rank %i before executing the function'%rank
		if not rank:
			#print 'rank %i executing the function'%rank
			result = func(*args, **kwargs)
		else:
			result = None
		#print 'rank %i before the barrier'%rank
		orbit_mpi.MPI_Barrier(comm)
		#print 'rank %i after the barrier'%rank
		return result
	return call