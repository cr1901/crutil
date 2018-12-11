import sympy as sym
from sympy.polys.orderings import monomial_key

# Symbolic expression to Python-control transfer function
def sym_to_tf(sym_expr):
    num, den = sym_expr.as_numer_denom()
    try:
        tf_num = [float(n) for n in sorted(sym.Poly(num, s).all_coeffs(), key=monomial_key('grlex', [s]))]
        tf_den = [float(d) for d in sorted(sym.Poly(den, s).all_coeffs(), key=monomial_key('grlex', [s]))]
    except sym.PolynomialError:
        raise ValueError("Only s variable must remain in input expression.")
    return ctl.tf(tf_num, tf_den)

# Convert Python-control analog transfer function to scipy-compatible num/den.
def tf_to_sp_analog(ctl_tf):
    temp = ctl_tf.returnScipySignalLti()[0][0]
    return (temp.num, temp.den)

# Convert Python-control digital transfer function to scipy-compatible b/a.
# Python-control has digital support, but I don't use it- unfamiliarity problem :P.
def tf_to_sp_digital(ctl_tf):
    raise NotImplementedError

# Convert Python-control analog transfer function to scipy-compatible b/a from prototype analog filter.
def tf_to_sp_bilinear(ctl_tf, fs=1.0):
    return sp.bilinear(*tf_to_sp_analog(ctl_tf), fs)

# Provide wrappers to convert directly from symbolic expression to scipy.
def sym_to_sp_analog(sym_expr):
    return tf_to_sp_analog(sym_to_tf(sym_expr))

def sym_to_sp_bilinear(sym_expr, fs=1.0):
    return tf_to_sp_bilinear(sym_to_tf(sym_expr), fs)
