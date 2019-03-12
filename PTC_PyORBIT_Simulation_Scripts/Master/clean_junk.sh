#!/bin/bash

# condor cleanup
mkdir Condor_Logfiles
mv output/simulation_info_* Condor_Logfiles
mv logfile_* Condor_Logfiles
mv output_* Condor_Logfiles

# clean ghost files
rm PTC/*~
rm Input/*~

# ptc cleanup
rm junk.txt
rm Maxwellian_bend_for_ptc.txt
rm Negative_node.OUT
