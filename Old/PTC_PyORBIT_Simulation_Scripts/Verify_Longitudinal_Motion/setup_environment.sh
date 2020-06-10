# script to setup the PyOrbit environment 
# execute like: . setup_environment.sh

pyOrbit_dir=/afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit

source ${pyOrbit_dir}/customEnvironment.sh
echo "customEnvironment done"
source ${pyOrbit_dir}/../virtualenvs/py2.7/bin/activate
echo "python packages charged"
source ${pyOrbit_dir}/../setup_ifort.sh
echo "ifort charged (necessary for running)"


ORBIT_ROOT_fullpath=`readlink -f ${ORBIT_ROOT}` 
echo 
echo "*****************************************************"
echo 
echo "full PyOrbit path:  ${ORBIT_ROOT_fullpath}"
echo
. ${ORBIT_ROOT}/../CheckGitStatus.sh ${ORBIT_ROOT_fullpath}

