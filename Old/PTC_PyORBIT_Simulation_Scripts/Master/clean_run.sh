#!/bin/bash

# Pickle and output files
rm -r output
rm -r bunch_output
rm -r lost
rm -r input

rm ptc_twiss
rm madx_twiss.tfs
rm PTC-PyORBIT_flat_file.flt
rm tunespread.dat

. clean_junk.sh
