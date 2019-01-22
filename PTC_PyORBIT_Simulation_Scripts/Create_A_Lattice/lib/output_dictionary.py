import time
import orbit_mpi
import scipy.io as sio

# 04.06.2017: added "import_from_matfile"

class Output_dictionary(object):

	def __init__(self, output_dictionary = None):
		if output_dictionary:
			print "to be implemented ... "
		else:
			self.entries = []
			self.parameter_functions = {}
			self.output_dict = {}
		self.print_header_flag = 1
		
	def addParameter(self, key, parameter_function):
		self.entries.append(key)
		self.parameter_functions[key] = parameter_function
		if not self.output_dict.has_key(key):
			self.output_dict[key] = []
	
	def getParameter(self, key):
		return self.output_dict[key]
		
	def update(self):
		rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		if not rank:
			map(lambda key: self.output_dict[key].append(self.parameter_functions[key]()), self.entries)
			if self.print_header_flag: 
				self.print_header()
				self.print_header_flag = 0
			self.print_last()
		
	def print_last(self):
		print ' '.join(map(lambda i: str(self.output_dict[i][-1]).ljust(18), self.entries)), time.strftime("%Y-%m-%d %H:%M:%S")

	def print_header(self):
		print ' '.join(map(lambda i: i.ljust(18), self.entries)), 'execution time'.ljust(10)

	def save_to_matfile(self, filename):
		rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		if not rank:
			sio.savemat(filename, self.output_dict)
		orbit_mpi.MPI_Barrier(orbit_mpi.mpi_comm.MPI_COMM_WORLD)

	def import_from_matfile(self, filename):
		d = sio.loadmat(filename, squeeze_me=True)
		for k in self.output_dict:
			self.output_dict[k] = d[k].tolist()
