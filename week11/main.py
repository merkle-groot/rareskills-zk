from srs import generate_srs, evaluate_on_srs
from py_ecc.bn128 import curve_order, G1, G2, pairing, eq
from galois import GF, lagrange_poly, Poly
from r1cs import get_qap, sanitize_matrix, check_input
from circuit import L, R, O, w
import numpy as np

def multiply_by_witness(polys, witness):
    new_polys = []
    for i in range(len(witness)):
        new_polys.append(polys[i] * witness[i])
    
    return new_polys

def get_vanishing_poly(degree, contraint_count, mod, GF):
    vanishing_poly = Poly([1], field=GF)
    for i in range(1, contraint_count+1):
        vanishing_poly = vanishing_poly*Poly([1, (-i) % mod], field=GF)
        print("i: ", Poly([1, (-i) % mod], field=GF), curve_order)
    return vanishing_poly

def get_ht(l_w, r_w, o_w, contraint_count, mod, GF):
    l_w_sum = Poly([0], field=GF)
    r_w_sum = Poly([0], field=GF)
    o_w_sum = Poly([0], field=GF)

    for i in range(len(l_w)):
        l_w_sum += l_w[i]
        r_w_sum += r_w[i]
        o_w_sum += o_w[i]

    numerator = l_w_sum * r_w_sum - o_w_sum
    denominator = get_vanishing_poly(len(l_w), contraint_count, mod, GF)

    h = numerator // denominator
    remainder = numerator % denominator
    ht = h * denominator
    
    if remainder != 0:
        raise ValueError("Error in calculating ht")
    return ht


if __name__ == "__main__":
    GF = GF(curve_order, primitive_element=5, verify=False)

    # initial setup, r1cs, qap
    (l_polys, r_polys, o_polys) = get_qap(L, R, O, GF, curve_order)
    w = sanitize_matrix(w, curve_order)
    check_input(L, R, O, w)

    # Trusted setup
    contraint_count = len(L)
    degree = len(l_polys)
    (g1_points, g2_points) = generate_srs(degree, curve_order, G1, G2)

    # evaluate qap on srs
    l_w = multiply_by_witness(l_polys, w)
    r_w = multiply_by_witness(r_polys, w)
    o_w = multiply_by_witness(o_polys, w)
    ht = get_ht(l_w, r_w, o_w, contraint_count, curve_order, GF)

    l_point = evaluate_on_srs(l_w, g1_points, degree, G1, GF)
    r_point = evaluate_on_srs(r_w, g2_points, degree, G2, GF)
    o_point = evaluate_on_srs(o_w, g1_points, degree, G1, GF)

    # print(ht)
    # ht_point = evaluate_on_srs(ht, g1_points, len(ht), G1, GF)


    lhs = pairing(r_point, l_point)
    rhs = pairing(G2, o_point)

    print(lhs)
    print(rhs)

    if not eq(lhs, rhs):
        raise ValueError("invalid pairing")
    else:
        print("pairing works!")

    print(list(reversed(l_w[4].coeffs)))
    print(l_point)

    