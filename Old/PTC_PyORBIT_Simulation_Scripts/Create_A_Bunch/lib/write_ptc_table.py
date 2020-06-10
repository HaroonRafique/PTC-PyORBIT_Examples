import numpy as np
import orbit_mpi

def write_RFtable(filename, harmonic_factors, time, E_kin, RF_voltage, RF_phase):
    comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
    rank = orbit_mpi.MPI_Comm_rank(comm)
    if not rank:
        n_lines = len(time)
        n_harmonics = len(harmonic_factors)
        arr = np.vstack((time,E_kin, np.dstack((RF_voltage,RF_phase)).flatten().reshape(n_lines, 2*n_harmonics).T)).T    
        with open(filename, 'w') as fid:
            fid.write('%d  1  1  0  %d\n'%(n_lines, n_harmonics))
            fid.write('  '.join(map(lambda i: '%d'%i, harmonic_factors))+'\n')
            for j in xrange(n_lines):
                fid.write('\t'.join(map(lambda i: '%1.8f'%i, arr[j, :]))+'\n')
    orbit_mpi.MPI_Barrier(comm)

def write_PTCtable(filename, multipole_orders, time, normal_components, skew_components):
    comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
    rank = orbit_mpi.MPI_Comm_rank(comm)
    factor = 1./np.math.factorial(multipole_orders-1) # the factorial factor is needed to be consistent with MADX
    if not rank:
        n_lines = len(time)
        n_multipoles = 1 # number of multipole orders to be changed (for the moment only 1 is implemented)
        arr = np.vstack((time,normal_components*factor,skew_components*factor)).T    
        with open(filename, 'w') as fid:
            fid.write('%d  1  %d\n'%(n_lines, n_multipoles))
            fid.write('  %d\n'%multipole_orders)
            for j in xrange(n_lines):
                fid.write('\t'.join(map(lambda i: '%1.11f'%i, arr[j, :]))+'\n')
    orbit_mpi.MPI_Barrier(comm)
    