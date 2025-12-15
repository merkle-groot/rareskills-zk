from srs import generate_srs, evaluate_poly_srs, evaluate_list_srs, get_vanishing_poly
from py_ecc.bn128 import curve_order, G1, G2, pairing, multiply, add, neg, eq
from galois import GF, Poly
from r1cs import get_qap, sanitize_matrix, check_input
from circuit import L, R, O, w, public_param_count
import numpy as np
from random import randint

def multiply_by_witness(polys, witness):
    new_polys = []
    for i in range(len(polys)):
        new_polys.append(polys[i] * witness[i])
    
    return new_polys

def evaluate_psi_srs_private(public_param_count, witness, psi_points_private, G1):
    return evaluate_psi_srs(witness[public_param_count:], psi_points_private, G1)

def evaluate_psi_srs_public(public_param_count, witness, psi_points_public, G1):
    return evaluate_psi_srs(witness[:public_param_count], psi_points_public, G1)

def evaluate_psi_srs(witness, psi_points, G):
    result = multiply(G, 0)
    for i in range(len(psi_points)):
        result = add(result, multiply(psi_points[i], witness[i]))

    return result

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
    public_param_count = public_param_count

    print("no of constraints: ", contraint_count)
    print("no of signals: ", term_nos)
    (
        g1_points, 
        g2_points, 
        ht_points, 
        alpha_1,
        beta_1,
        beta_2, 
        delta_1, 
        delta_2, 
        gamma_2, 
        psi_points_public, 
        psi_points_private
    ) = generate_srs(
        contraint_count, 
        public_param_count,
        curve_order, 
        l_polys,
        r_polys,
        o_polys,
        GF, 
        G1, 
        G2
    )

    # print("psi_points_public: ", psi_points_public)
    # print("psi_points_private: ", psi_points_private)

    # # evaluate qap on srs
    print("multiply qap by witness...")
    l_w = multiply_by_witness(l_polys, w)
    r_w = multiply_by_witness(r_polys, w)
    o_w = multiply_by_witness(o_polys, w)

    print("generating h...")
    h = get_h(l_w, r_w, o_w, contraint_count, curve_order, GF)
    print("h generated")

    print("evaluate qap on srs...")
    l_point = evaluate_list_srs(l_w, g1_points, G1, GF)
    r_point_1 = evaluate_list_srs(r_w, g1_points, G1, GF)
    r_point_2 = evaluate_list_srs(r_w, g2_points, G2, GF)
    o_point = evaluate_list_srs(o_w, g1_points, G1, GF)
    h_point = evaluate_poly_srs(h, ht_points, G1, GF)

    psi_private_point = evaluate_psi_srs_private(public_param_count, w, psi_points_private, G1)

    # print("psi_points_private: ", psi_points_private)
    # print("witness: ", w)
    # print("psi_private_point: ", psi_private_point)
    
    r = randint(0, curve_order)
    s = randint(0, curve_order)

    # a_1 = alpha_1 + l_point_1 + r * delta_1
    A_1 = add(
        alpha_1, 
        add(
            l_point,
            multiply(delta_1, r)
        )
    )
    
    # b_1 = beta_1 + r_point_1 + s * delta_1
    B_1 = add(
        beta_1,
        add(
            r_point_1,
            multiply(delta_1, s)
        )
    )

    # b_2 = beta_2 + r_point_2 + s * delta_2
    B_2 = add(
        beta_2,
        add(
            r_point_2,
            multiply(delta_2, s)
        )
    )

    # for negative rs
    rs = int(-(GF(r) * GF(s)))

    # salt = s*A_1 + r*B_1 - rs*del_1
    salt_component_point = add(
        multiply(A_1, s),
        add(
            multiply(B_1, r),
            multiply(delta_1, rs)
        )
    )
    # c = psi_private_1 + h_point1 + s*A_1 + r*B_1 - rs*delta_1
    C_1 = add(
        psi_private_point,
        add(
            h_point,
            salt_component_point
        )
    )

    # verifier
    psi_public_point = evaluate_psi_srs_public(public_param_count, w, psi_points_public, G1)
    print("performing pairing...")
    pairing_1 = pairing(B_2, neg(A_1))
    pairing_2 = pairing(beta_2, alpha_1)
    pairing_3 = pairing(gamma_2, psi_public_point)
    pairing_4 = pairing(delta_2, C_1)

    print("pairing done")

    result = pairing_1 * pairing_2 * pairing_3 * pairing_4
    expected_result = pairing(G2, multiply(G1, 0))

    assert eq(result, expected_result)
    print("proof succesfull")

    