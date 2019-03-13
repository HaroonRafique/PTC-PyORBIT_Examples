#!/bin/bash
source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit/customEnvironment.sh
echo "customEnvironment done"
source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/virtualenvs/py2.7/bin/activate
echo "python packages charged"
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/setup.sh
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/ifortvars.sh intel64
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/iccvars.sh intel64
echo "ifort charged (necessary for running)"

