from srs import generate_srs, evaluate_poly_srs, evaluate_list_srs, get_vanishing_poly
from py_ecc.bn128 import curve_order, G1, G2, pairing, multiply, add, neg, eq
from galois import GF, Poly
from r1cs import get_qap, sanitize_matrix, check_input
from circuit import L, R, O, w
import numpy as np

def multiply_by_witness(polys, witness):
    new_polys = []
    for i in range(len(polys)):
        new_polys.append(polys[i] * witness[i])
    
    return new_polys


def get_h(l_w, r_w, o_w, contraint_count, mod, GF):
    l_w_sum = Poly([0], field=GF)
    r_w_sum = Poly([0], field=GF)
    o_w_sum = Poly([0], field=GF)

    for i in range(len(l_w)):
        l_w_sum += l_w[i]
        r_w_sum += r_w[i]
        o_w_sum += o_w[i]

    numerator = l_w_sum * r_w_sum - o_w_sum
    denominator = get_vanishing_poly(contraint_count, mod, GF)

    h = numerator // denominator
    remainder = numerator % denominator

    if remainder != 0:
        raise ValueError("Error in calculating ht")
    return h


if __name__ == "__main__":
    GF = GF(curve_order, primitive_element=5, verify=False)

    # initial setup, r1cs, qap
    (l_polys, r_polys, o_polys) = get_qap(L, R, O, GF, curve_order)
    w = sanitize_matrix(w, curve_order)
    check_input(L, R, O, w)

    # Trusted setup
    contraint_count = len(L)
    term_nos = len(l_polys)

    print("no of constraints: ", contraint_count)
    print("no of signals: ", term_nos)
    (g1_points, g2_points, ht_points) = generate_srs(contraint_count, curve_order, GF, G1, G2)

    # evaluate qap on srs
    print("multiply qap by witness...")
    l_w = multiply_by_witness(l_polys, w)
    r_w = multiply_by_witness(r_polys, w)
    o_w = multiply_by_witness(o_polys, w)
    print("generating h...")
    h = get_h(l_w, r_w, o_w, contraint_count, curve_order, GF)
    print("h generated")

    print("evaluate qap on srs...")
    l_point = evaluate_list_srs(l_w, g1_points, G1, GF)
    r_point = evaluate_list_srs(r_w, g2_points, G2, GF)
    o_point = evaluate_list_srs(o_w, g1_points, G1, GF)
    h_point = evaluate_poly_srs(h, ht_points, G1, GF)
    print("qap evaluated")

    print("performing pairing...")
    pairing_1 = pairing(r_point, neg(l_point))
    pairing_2 = pairing(G2, add(o_point, h_point))
    print("pairing done")

    result = pairing_1 * pairing_2 
    expected_result = pairing(G2, multiply(G1, 0))

    assert eq(result, expected_result)
    print("proof succesfull")

    