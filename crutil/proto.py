import scipy.signal as sp
import sympy as sym

import crutil.control as crctl

# z, s, T, t, alpha, beta, gamma, tau1, tau2 = sym.symbols('z s T t alpha beta gamma tau_1 tau_2')

def sym_bilinear(sym_expr, T_0=None):
    T = sym.symbols("T")
    xform = (2/T)*(z - 1)/(z + 1)
    if not T_0:
        return sym_expr.subs(s, xform)
    else:
        xform_T = xform.subs(T, T_0)
        return sym_expr.subs(s, xform_T)

def sym_inverse_bilinear(sym_expr, T_0=None):
    T = sym.symbols("T")
    inv = (1 + (s*T/2))/(1 - (s*T/2))
    if not T_0:
        return sym_expr.subs(z, inv)
    else:
        inv_T = inv.subs(T, T_0)
        return sym_expr.subs(z, inv_T)

def proto_digital_compare(proto, w, fs=1.0):
    num, den = crctl.tf_to_sp_analog(proto)
    bd, ad = crctl.tf_to_sp_bilinear(proto, fs)
    return analog_digital_compare((num, den), (bd, ad), w, fs)

def analog_digital_compare(analog, digital, w, fs=1.0):
    wa, ha = sp.freqs(analog[0], analog[1], w) # Get s-domain response of analog filter.
    wd_calc = wa/fs # Normalize Nyquist freq to pi (rads elapsed).
    _, hd = sp.freqz(digital[0], digital[1], wd_calc) # Get z-domain at equivalent analog freqs, since sample rate is known.
    return (wa, ha, hd)
