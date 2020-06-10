import numpy as np
from scipy import constants as const
from sys import stdout
from itertools import product
import readline
import argparse

def parse_main_args(parser):
    parser.add_argument('-i', action='store_true',
            help='counter-check parameters to be used in the ' +
                                            'calculation interactively')
    parser.add_argument('-v', action='store_true',
            help='show progress while reading files and calculating ' +
                        'and print brushed up output')
    parser.add_argument('files', nargs='+',
            help='TWISS files to be processed')
    parser.add_argument('--labels', action='store_true',
            help='print labels of columns for standard table output')
    parser.add_argument('--coasting', action='store_true',
            help='assume coasting beam, sig_z / bunch_length will be '
            'ignored') # don't add this to the parameter names
    param_names = add_param_args(parser)
    args = parser.parse_args()
    if args.v:
        print ''
        stdout.write(" " * 9 + "progress:\n" + "=" * (9 + 9) + "\n")
    params = {'coasting': args.coasting}
    for pn in param_names:
        attr = getattr(args, pn)
        if attr:
            params[pn] = attr[0]
    return args, params

def add_param_args(parser):
    '''Add all additional possible parameters to the parser.
    These parameters are used to override what is read from the TWISS
    file. Return the names of parameters.
    '''
    parser.add_argument(
        '--machine', nargs=1, metavar='identification',
        help='override machine identification read from the '
        'TWISS file by the given argument value')
    parser.add_argument(
        '--mass', nargs=1, type=float, metavar='float',
        help='override "MASS" value read from the TWISS file by '
        'the given mass value [GeV]')
    parser.add_argument(
        '--n_charges_per_part', nargs=1, type=float, default=[1.0],
        metavar='float',
        help='number of elementary charges per particle (default value 1.0)')
    parser.add_argument(
        '--gamma', nargs=1, type=float, metavar='float',
        help='override "GAMMA" value read from the TWISS file by '
        'the given gamma value')
    parser.add_argument(
        '--sig_z', nargs=1, type=float, metavar='float',
        help='override "SIGT" value read from the TWISS file by '
        'the given sig_z value [m]')
    parser.add_argument(
        '--n_part', nargs=1, type=float, metavar='float',
        help='override "NPART" value read from the TWISS file by '
        'the given n_part value')
    parser.add_argument(
        '--emit_norm_tr', nargs=1, type=float, metavar='float',
        help='use this normalized emittance value [m] for both '
        'horizontal and vertical plane as first priority')
    parser.add_argument(
        '--emit_norm_x', nargs=1, type=float, metavar='float',
        help='use this normalized emittance value [m] for '
        'the horizontal plane as first priority')
    parser.add_argument(
        '--emit_norm_y', nargs=1, type=float, metavar='float',
        help='use this normalized emittance value [m] for '
        'the vertical plane as first priority')
    parser.add_argument(
        '--emit_geom_x', nargs=1, type=float, metavar='float',
        help='override "EX" value read from the TWISS file by '
        'the given emit_geom_x value [m]')
    parser.add_argument(
        '--emit_geom_y', nargs=1, type=float,
        metavar='float',
        help='override "EY" value read from the TWISS file by '
        'the given emit_geom_y value [m]')
    parser.add_argument(
        '--deltaE', nargs=1, type=float, metavar='float',
        help='override "SIGE" value read from the TWISS file by '
        'the given deltaE value')
    parser.add_argument(
        '--lshape', nargs=1, type=float, default=[1.0], metavar='float',
        help='shape factor e.g. to account for dual harmonic '
        '(default value 1.0)')
    parser.add_argument(
        '--Ekin', nargs=1, type=float, metavar='float',
        help='use this kinetic energy value [GeV] as first priority')
    parser.add_argument(
        '--deltap', nargs=1, type=float, metavar='float',
        help='use this delta_p/p value as first priority')
    parser.add_argument(
        '--bunch_length', nargs=1, type=float, metavar='float',
        help='use this bunch_length value [ns] as first priority')
    return (
        'machine', 'mass', 'n_charges_per_part', 'gamma', 'sig_z', 'n_part',
        'emit_norm_x', 'emit_norm_y', 'emit_geom_x', 'emit_geom_y',
        'emit_norm_tr', 'deltaE', 'lshape', 'Ekin', 'deltap', 'bunch_length'
    )

def confirm_filenames(filenames):
    fnp = '; '.join(filenames)
    readline.set_startup_hook( lambda: readline.insert_text(fnp) )
    try:
        raw_list = raw_input("\nPlease enter the twiss file names" +
                                        " separated by semicola:\n\n")
        return [ item.strip() for item in raw_list.split(';') ]
    except:
        print "Error: faulty input, using %s instead!" % str(filenames)
        return filenames
    finally:
        readline.set_startup_hook()
        print ""

def get_content_length(filename):
    source = open(filename, "r")
    n_content_lines = 0
    for line in source:
        if line.split()[0] not in ["@", "*", "$"]:
            n_content_lines += 1
    if n_content_lines == 0:
        raise IOError("Could not identify twiss data contents in file" +
                        filename + "!")
    source.close()
    return n_content_lines

def evaluate_headers(sources, inputs):
    translation = { "MASS": "mass",
                    "GAMMA": "gamma", "SIGT": "sig_z",
                    "NPART": "n_part", "EX": "emit_geom_x",
                    "EY": "emit_geom_y", "SIGE": "deltaE" }
    for src in sources:
        src.seek(0, 0)
        line = src.readline()
        while line[0] == "@":
            fields = line.split()
            if fields[1] == "SEQUENCE":
                inputs["machine"] = fields[3].strip('"')
            for twiss_var, trans in translation.iteritems():
                if fields[1] == twiss_var and not inputs[trans]:
                    inputs[trans] = float(fields[3])
            line = src.readline()
    return inputs

def advance_to_col_def(source):
    source.seek(0, 0)
    last_pos = source.tell()
    while source.readline()[0] is not "*":
        last_pos = source.tell()
    source.seek(last_pos)
    return source

def parse_cols(col_description_lines):
    columns = dict()
    for line in col_description_lines:
        assert line[0] == "*"
    col_madx_names = { "s": ["S"],
                       "beta_x": ["BETX", "BETA11"],
                       "beta_y": ["BETY", "BETA22"],
                       "d_x": ["DX", "DISP1"],
                       "d_y": ["DY", "DISP2"] }
    fields = [line.split() for line in col_description_lines]
    for var, synonyms in col_madx_names.iteritems():
        for syn, i_file in product(synonyms, xrange(len(fields))):
            try:
                # -1 due to additional asterisk field in the line
                col = fields[i_file].index(syn) - 1
                break
            except ValueError:
                col = -1
        else:
            i_file = None
            if not f_interactive:
                raise ValueError(str(synonyms) +
                                    " not found in column headings")
        columns[var] = (i_file, col)
    return columns

def advance_to_contents(source):
    last_pos = source.tell()
    while source.readline()[0] in ["@", "*", "$"]:
        last_pos = source.tell()
    source.seek(last_pos)
    return source

def fill_data(lines, columns, data):
    fields = [ l.split() for l in lines ]
    for var, coltuple in columns.iteritems():
        value = fields[ coltuple[0] ][ coltuple[1] ]
        data[var].append( float(value) )
    return data

def confirm_inputs(inputs):
    print ""
    for key, value in iter(sorted(inputs.iteritems())):
        readline.set_startup_hook( lambda: readline.insert_text(str(value)) )
        try:
            if type(value) is float:
                value = float( raw_input("Please enter " +
                            "(float) parameter " + key + ": ") )
            else:
                value = raw_input("Please enter parameter " +
                                                            key + ": ")
        finally:
            readline.set_startup_hook()
        inputs[key] = value
    print ""
    return inputs

def check_data_integrity(data, inputs):
    assert (len(data["s"]) == len(data["beta_x"]))
    assert (len(data["beta_x"]) == len(data["beta_y"]))
    assert (len(data["beta_y"]) == len(data["d_x"]))
    assert (len(data["d_x"]) == len(data["d_y"]))
    assert (inputs["gamma"] > 1.0)
    if not inputs.get('coasting', False):
        assert (inputs["sig_z"] != 0.0)

def complete(data, inputs):
    '''Determine the priorities for overriding parameters w.r.t each
    other and the inputs read from the TWISS file.
    '''
    if "Ekin" in inputs:
        inputs["gamma"] = inputs["Ekin"] / inputs["mass"] + 1.0
    else:
        inputs["Ekin"] = (inputs["gamma"] - 1) * inputs["mass"]
    inputs["beta"] = np.sqrt(1.0 - 1.0 / inputs["gamma"]**2)
    if "deltap" in inputs:
        inputs["deltaE"] = (inputs["beta"] * inputs["beta"] *
                                                    inputs["deltap"] )
    else:
        inputs["deltap"] = ( inputs["deltaE"] /
                                ( inputs["beta"] * inputs["beta"] ) )
    if inputs.get("coasting", False):
        circumference = data["s"][-1]
        inputs["sig_z"] = circumference
        inputs.pop("bunch_length", None)
    if "bunch_length" in inputs:
        inputs["sig_z"] = ( 1.0e-9 * inputs["beta"] * const.c *
                                inputs["bunch_length"] / 4.0 )
    else:
        inputs["bunch_length"] = ( 4.0 * inputs["sig_z"] /
                                ( 1.0e-9 * inputs["beta"] * const.c ) )
    if "emit_norm_tr" in inputs:
        inputs["emit_norm_x"] = inputs["emit_norm_tr"]
        inputs["emit_norm_y"] = inputs["emit_norm_tr"]
        inputs["emit_geom_x"] = ( inputs["emit_norm_x"] /
                                ( inputs["gamma"] * inputs["beta"] ) )
        inputs["emit_geom_y"] = ( inputs["emit_norm_y"] /
                                ( inputs["gamma"] * inputs["beta"] ) )
    else:
        if 'emit_norm_x' in inputs:
            inputs["emit_geom_x"] = (inputs["emit_norm_x"] /
                                     (inputs["gamma"] * inputs["beta"] ))
        else:
            inputs["emit_norm_x"] = ( inputs["emit_geom_x"] *
                                    inputs["gamma"] * inputs["beta"] )
        if 'emit_norm_y' in inputs:
            inputs["emit_geom_y"] = (inputs["emit_norm_y"] /
                                     (inputs["gamma"] * inputs["beta"] ))
        else:
            inputs["emit_norm_y"] = ( inputs["emit_geom_y"] *
                                    inputs["gamma"] * inputs["beta"] )
    return data, inputs

def get_source_program(filename):
    source = open(filename, "r")
    fields = source.readline().split()
    while fields[0] == "@":
        if fields[1] == "NAME":
            if fields[3] == '"PTC_TWISS"':
                return "PTC"
            elif fields[3] == '"TWISS"':
                return "MADX"
            else:
                break
        fields = source.readline().split()
    return "notfound"

def correct_madx_dispersion(data, inputs):
    # correcting for ( dispersion / beta ) output from MAD-X,
    # make sure this is done as long as the gamma is still
    # the one taken from the MADX file (and not yet overwritten by
    # complete() with the prioritized command line argument value)
    inputs["beta"] = np.sqrt(1.0 - 1.0 / inputs["gamma"]**2)
    data["d_x"][:] = [ d * inputs["beta"] for d in data["d_x"] ]
    data["d_y"][:] = [ d * inputs["beta"] for d in data["d_y"] ]
    return data

def get_inputs(filenames, params, f_interactive=False, f_verbose=False):
    """obtains parameters and TWISS data from the MAD-X or PTC TWISS files
        <i>filenames</i> (usually ending on .tfs) and returns
        dictionaries / hash tables <i>inputs</i> and <i>data</i>
        containing all required data for calculating the space charge
        tune shift with the function calc_tune_spread. Parameters are
        taken from the files with descending priority. Parameters
        defined by <i>params</i> override parameters read from the
        TWISS files."""
    if f_interactive:
        filenames = confirm_filenames(filenames)
    n_content_lines = get_content_length(filenames[0])
    inputs = {
        "machine": None, "mass": None, "n_part": None,
        "lshape": None, "emit_geom_x": None, "emit_geom_y": None,
        "gamma": None, "deltaE": None, "sig_z": None,
        "coasting": params.get('coasting', False),
        "n_charges_per_part": None,
    }
    data = {"s": [], "beta_x": [], "beta_y": [], "d_x": [], "d_y": [] }
    sources = [open(fn, "r") for fn in filenames]
    #for fn in filenames:
    #    assert n_content_lines == get_content_length(fn)
    # twiss file header part:
    inputs = evaluate_headers(sources, inputs)
    for src in sources:
        advance_to_col_def(src)
    columns = parse_cols( [ src.readline() for src in sources ] )
    for src in sources:
        advance_to_contents(src)
    # twiss file content part
    current_content_line = 0
    while current_content_line < n_content_lines:
        data = fill_data( [ src.readline() for src in sources ],
                                                        columns, data)
        current_content_line += 1
        if f_verbose:
            stdout.write("\rread twiss %.2f%% (item %d out of %d)" %
                    (100.0 * current_content_line / n_content_lines,
                            current_content_line, n_content_lines) )
            stdout.flush()
    if f_verbose:
        stdout.write("\n")
    for src in sources: src.close()
    inputs.update(params)
    if f_interactive:
        inputs = confirm_inputs(inputs)
    for key, value in inputs.iteritems():
        # complain if no value is set, ignore sig_z for a coasting beam
        if (value is None) and not (key is 'sig_z' and inputs['coasting']):
            raise NameError(key + " has not been set appropriately!")
    check_data_integrity(data, inputs)
    source_program = get_source_program(filenames[0])
    if source_program is "MADX":
        data = correct_madx_dispersion(data, inputs)
        if f_verbose:
            print ("INFO: corrected for MADX dispersion convention via "
                   "multiplying DX / DISP1 by the relativistic beta.")
    elif source_program is "notfound":
        print ("\nWARNING: source program (@NAME) could not be " +
                "detected! No correction of relativistic beta " +
                "normalized dispersion functions (occuring in " +
                "MADX output) has been performed, the dispersion " +
                "has been used as defined in the first TWISS file. \n")
    data, inputs = complete(data, inputs)
    return data, inputs

def print_verbose_output(inputs, data, DeltaQ_x, DeltaQ_y):
    heading_param = "      used parameters for the %s:" % inputs["machine"]
    print heading_param + "\n" + "=" * len(heading_param)
    print " rest mass of particle [GeV]: %g" % inputs["mass"]
    print "      # charges per particle: %g" % inputs["n_charges_per_part"]
    print "          relativistic gamma: %g" % inputs["gamma"]
    print "number of particles in bunch: %g" % inputs["n_part"]
    print "rms bunch length sigma_z [m]: %g" % inputs["sig_z"]
    print "    momentum spread deltap/p: %.6g" % inputs["deltap"]
    print "  normalized emittance_x [m]: %g" % inputs["emit_norm_x"]
    print "  normalized emittance_y [m]: %g" % inputs["emit_norm_y"]
    print "           circumference [m]: %g" % data["s"][-1]
    heading_res = "      tune spread due to space charge:"
    print "\n" + heading_res + "\n" + "=" * len(heading_res)
    print "        DeltaQ_x = %.6g" % DeltaQ_x
    print "        DeltaQ_y = %.6g\n" % DeltaQ_y

def print_table_output(inputs, data, DeltaQ_x, DeltaQ_y, f_labels):
    if f_labels:
        print "\t".join(("# N_p ", "B_length [ns] ", "E_kin [GeV] ",
                            "deltap/p ", "norm emit_x [m] ",
                            "norm emit_y [m] ", "DeltaQ_x ",
                            "DeltaQ_y" ))
    print "%g\t%g\t%g\t%g\t%g\t%g\t%g\t%g" % (inputs["n_part"],
                        inputs["bunch_length"], inputs["Ekin"],
                        inputs["deltap"], inputs["emit_norm_x"],
                        inputs["emit_norm_y"], DeltaQ_x, DeltaQ_y)