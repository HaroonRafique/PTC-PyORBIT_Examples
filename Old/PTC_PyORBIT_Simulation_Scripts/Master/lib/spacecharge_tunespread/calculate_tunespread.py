from tunespread import *

gamma = 1.012149995
beta = np.sqrt(gamma**2-1)/gamma

deltap = 2.5e-4/3.

emit_x = (beta*gamma)*12.57e-6 / 4.
emit_y = (beta*gamma)*9.3e-6 / 4.

q = 1

# ~ n_part = 0.305564e11		# dQx = 0.01
# ~ n_part = 2.95e10 				# dQx = 0.097
# ~ blength = 3472.7

# ~ n_part = 2.03706e9			# dQx = 0.01
n_part = 2.0e9			# dQx = 0.01
blength = 231.51

'''
Step2+
n_part = 2e11
blength = 3472.7
Step5+
n_part = 1.3e10
blength = 231
'''

twissfile = ['ptc_twiss_matched.tfs']
params = {'n_part': n_part, 'emit_norm_x': emit_x, 'emit_norm_y': emit_y, 'gamma': gamma,
          'deltap': deltap, 'n_charges_per_part': q, 'lshape':1., 'bunch_length': blength, 'coasting': False} 
data, inputs = ext.get_inputs(twissfile, params, False, False)
dQ = calc_tune_spread(data, inputs)
print inputs
ext.print_verbose_output(inputs, data, dQ[0], dQ[1])
print "dQx = %2.3f, dQy = %2.3f"%(dQ[0], dQ[1])

