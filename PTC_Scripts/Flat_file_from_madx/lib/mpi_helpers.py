import orbit_mpi
import os


def only_main_rank(func):
	def call(*args, **kwargs):
		comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
		rank = orbit_mpi.MPI_Comm_rank(comm)
		if not rank:
			result = func(*args, **kwargs)
		else:
			result = None
		orbit_mpi.MPI_Barrier(comm)
		return result
	return call

@only_main_rank
def mpi_mkdir_p(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)