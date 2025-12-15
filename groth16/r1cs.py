import numpy as np
from py_ecc.bn128 import curve_order
from galois import GF, lagrange_poly
import numpy as np

def sanitize_matrix(m, mod = curve_order):
    arr = np.array(m, dtype=object)
    arr %= mod
    return arr

def matrix_multiply_mod(a, b, mod = curve_order):
    return (a @ b) % mod

def hadamard_mod(a, b, mod = curve_order):
    return np.multiply(a, b) % mod

def check_input(l, r, o, w, mod = curve_order):
    l = sanitize_matrix(l, mod)
    r = sanitize_matrix(r, mod)
    o = sanitize_matrix(o, mod)
    w = sanitize_matrix(w, mod)

    left_mul = matrix_multiply_mod(l, w)
    right_mul = matrix_multiply_mod(r, w)
    output_mul = matrix_multiply_mod(o, w)

    left_right_mul = hadamard_mod(left_mul, right_mul, mod)

    result = output_mul == left_right_mul
    if not result.all():
        raise ValueError("Input validation failed: O*w != (L*w ∘ R*w) mod p")

    print("Initial r1cs check passed")
    return True

def get_poly(vec, GF):
    # print("interpolating y:", vec)
    xs = list(range(1, len(vec) + 1))
    # print("x coord: ", xs)
    return lagrange_poly(GF(xs), GF(vec))

def get_qap(l, r, o, GF, mod = curve_order):
    l = sanitize_matrix(l, mod)
    r = sanitize_matrix(r, mod)
    o = sanitize_matrix(o, mod)

    if l.shape != r.shape != o.shape:
        raise ValueError("matrix mismatch")
    l_polys = []
    r_polys = []
    o_polys = []
    for i in range(l.shape[1]):
        l_polys.append(
            get_poly(l[:, i], GF)
        )
        r_polys.append(
            get_poly(r[:, i], GF)
        )
        o_polys.append(
            get_poly(o[:, i], GF)
        )

    return (l_polys, r_polys, o_polys)

if __name__ == "__main__":
    GF = GF(curve_order, primitive_element=5, verify=False)
    # check_input(L, R, O, w)
    from circuit import L, R, O, w
    get_qap(L, R, O, GF)
# print(left_mul)
