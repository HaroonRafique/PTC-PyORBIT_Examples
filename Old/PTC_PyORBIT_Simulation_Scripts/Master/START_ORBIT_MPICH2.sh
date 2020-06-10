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

echo 'Setup environment'
. setup_environment.sh

echo 'ORBIT_ROOT = '
echo ${ORBIT_ROOT}

/afs/cern.ch/project/LIUsc/space_charge/Codes/mpich2-1.4.1p1/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
