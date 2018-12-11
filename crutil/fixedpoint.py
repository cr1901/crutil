import numpy as np

def float_to_fixed(flt, int_bits, exp_bits, float_repr=True):
    sign = np.sign(flt)
    mantissa = np.floor(np.abs(flt))
    exponent = np.round((sign*flt - mantissa) * 2**exp_bits)/(2**exp_bits)
    out = sign * (mantissa+exponent)

    max_int = 2**int_bits - 1
    s_mantissa = sign * mantissa
    # Infinite sign bits for negative numbers, so bitwise manip won't work.
    if s_mantissa >= max_int or s_mantissa < -(max_int + 1):
        raise OverflowError

    if not float_repr:
        out = out * (2**exp_bits)
        assert(out == int(out))
        out = int(out)
    return out

def truncate(bd, ad, int_bits, exp_bits, float_repr=True):
    dec = lambda p : float_to_fixed(p, int_bits, exp_bits, float_repr)
    bd_d = np.fromiter((dec(b) for b in bd), np.float)
    ad_d = np.fromiter((dec(a) for a in ad), np.float)
    return (bd_d, ad_d)
