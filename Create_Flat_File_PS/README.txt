MAD-X/PTC example of how to create a PTC Flat File for PTC-PyORBIT lattice definition.

Start with Instructions.ipynb

To open this file install jupyter and use the command:

$> jupyter notebook Instructions.ipynb &
(without the $> in front)

To run manually use the madx executable provided in the folder above 
like so to generate a PTC flat file readable by PyORBIT:

$> ../madx-linux64_v5_02_00 < Create_PTC_flat_file.madx
