# tool calculating the tune spread due to space charge based upon
# MAD-X or PTC Twiss files, for command line input options type
#   ~$ python tunespread.py --help
#
# created 2013 by Adrian Oeftiger, oeftiger@cern.ch
#

# constants
re = 2.8179403267e-15 # classical electron radius in [m]
me = 0.510998928e-3 # electron mass in [GeV]
mp = 0.938272046 # proton mass in [GeV]
rtimesm = re * me # class. radius to be divided by mass [m * GeV]

import libtunespread as ext

import numpy as np
from scipy import constants as const
from sys import stdout
import argparse

def run():
    runwith({})

def runwith(fixedparams):
    args, params = ext.parse_main_args(argparse.ArgumentParser())
    params.update(fixedparams)
    data, inputs = ext.get_inputs(args.files, params, args.i, args.v)
    DeltaQ_x, DeltaQ_y = calc_tune_spread(data, inputs, args.v)
    if args.v:
        ext.print_verbose_output(inputs, data, DeltaQ_x, DeltaQ_y)
    else:
        ext.print_table_output(inputs, data, DeltaQ_x, DeltaQ_y,
                                                        args.labels)

def calc_tune_spread(data, inputs, f_verbose=False):
    """Calculates the (maximum) tune shift DeltaQ_x and DeltaQ_y due
    to space charge with given optics parameters provided by
    the dictionaries / hash tables <i>inputs</i> and <i>data</i>.
    """
    r = rtimesm * inputs["n_charges_per_part"]**2 / inputs["mass"]
    beta = inputs["beta"]
    gamma = inputs["gamma"]
    sig_z = inputs.get("sig_z", None)
    n_part = inputs["n_part"]
    deltap = inputs["deltap"]
    emit_x = inputs["emit_geom_x"]
    emit_y = inputs["emit_geom_y"]
    lshape = inputs["lshape"]
    integx = integy = 0

    datalength = len(data["s"]) - 1        # -1 for ds (fencepost error)
    for step in xrange( datalength ):
        ds = data["s"][step + 1] - data["s"][step]
        beta_x = data["beta_x"][step]
        beta_y = data["beta_y"][step]
        d_x = data["d_x"][step]
        d_y = data["d_y"][step]

        sqx = np.sqrt(emit_x * beta_x + d_x**2 * deltap**2)
        sqy = np.sqrt(emit_y * beta_y + d_y**2 * deltap**2)
        integx += beta_x * ds / (sqx * (sqx + sqy))
        integy += beta_y * ds / (sqy * (sqx + sqy))
        if f_verbose:
            stdout.write("\rintegrated %.2f%% (item %d out of %d)" %
                            (100.0 * (step + 1) / datalength,
                                        step + 1, datalength) )
            stdout.flush()
    if f_verbose:
        stdout.write("\n\n")
    prefactor = r * n_part / (2.0 * const.pi * beta**2 * gamma**3)
    if inputs.get('coasting', False):
        circumference = data["s"][-1]
        shapefactor = lshape / circumference
    else:
        # assume Gaussian shape
        shapefactor = lshape / (np.sqrt(2.0 * const.pi) * sig_z)
    DeltaQ_x = prefactor * shapefactor * integx
    DeltaQ_y = prefactor * shapefactor * integy

    return (DeltaQ_x, DeltaQ_y)

if __name__ == "__main__":
    run()