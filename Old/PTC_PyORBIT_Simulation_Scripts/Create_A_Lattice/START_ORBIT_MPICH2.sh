#!/bin/bash

if [ ! -n "$1" ]
  then
    echo "Usage: `basename $0` <name of the SC script> <N CPUs>"
    exit $E_BADARGS
fi

if [ ! -n "$2" ]
  then
    echo "Usage: `basename $0` <name of the SC script> <N CPUs>"
    exit $E_BADARGS
fi

# Have to choose which PyORBIT to use:
#export ORBIT_ROOT=/afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit_frozenSC_20170731
#~ export ORBIT_ROOT=/afs/cern.ch/user/p/pyorbit/public/PyORBIT/py-orbit
#~ export ORBIT_ROOT=/afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit
#~ export ORBIT_ROOT=/afs/cern.ch/project/LIUsc/space_charge/Codes/py-orbit_revison1291_dev_FrozenPIC

#~ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${ORBIT_ROOT}/lib
#~ export PYTHONPATH=${PYTHONPATH}:${ORBIT_ROOT}/py:${ORBIT_ROOT}/lib
#~ export PATH=$PATH:${ORBIT_ROOT}/bin

#~ source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh
#source /afs/cern.ch/user/p/pyorbit/public/PyORBIT/py-orbit/customEnvironment.sh
#source /afs/cern.ch/user/p/pyorbit/public/PyORBIT/virtualenvs/py2.7/bin/activate

echo 'Setup environment'
. setup_environment.sh
#~ source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit_frozenSC_20170731/customEnvironment.sh
#~ echo "customEnvironment done"
#~ source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/virtualenvs/py2.7/bin/activate
#~ echo "python packages charged"
#~ source /cvmfs/projects.cern.ch/intelsw/psxe/linux/setup.sh
#~ source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/ifortvars.sh intel64
#~ source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/iccvars.sh intel64
#~ echo "ifort charged (necessary for running)"

echo 'ORBIT_ROOT = '
echo ${ORBIT_ROOT}

# /afs/cern.ch/project/LIUsc/space_charge/Codes/mpich-3.0/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
/afs/cern.ch/project/LIUsc/space_charge/Codes/mpich2-1.4.1p1/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
