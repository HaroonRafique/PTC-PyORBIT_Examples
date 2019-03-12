#!/bin/bash

. clean_run.sh
. clean_junk.sh

# ptc cleanup
rm flat.dat
rm SPACE_CHARGE_STUDIES_INJECTION.flt

# PyORBIT cleanup
rm -r input/
rm -r bunch_output/mainbunch*
rm output/output.mat
