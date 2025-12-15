from srs import generate_srs, evaluate_poly_srs, evaluate_list_srs, get_vanishing_poly
from py_ecc.bn128 import curve_order, G1, G2, multiply, add, neg
from galois import GF, Poly
from r1cs import get_qap, sanitize_matrix, check_input
import numpy as np
from random import randint


def multiply_by_witness(polys, witness):
    """Multiply polynomials by witness values"""
    new_polys = []
    for i in range(len(polys)):
        new_polys.append(polys[i] * witness[i])

    return new_polys


def evaluate_psi_srs(witness, psi_points, G):
    """Evaluate psi SRS points"""
    result = multiply(G, 0)
    for i in range(len(psi_points)):
        result = add(result, multiply(psi_points[i], witness[i]))

    return result


def evaluate_psi_srs_private(public_param_count, witness, psi_points_private, G1):
    """Evaluate psi SRS for private witness values"""
    return evaluate_psi_srs(witness[public_param_count:], psi_points_private, G1)


def evaluate_psi_srs_public(public_param_count, witness, psi_points_public, G1):
    """Evaluate psi SRS for public witness values"""
    return evaluate_psi_srs(witness[:public_param_count], psi_points_public, G1)


def get_h(l_w, r_w, o_w, contraint_count, mod, GF):
    """Calculate the h polynomial for the quotient"""
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


def generate_proof(l_polys, r_polys, o_polys, witness, public_param_count,
                   constraint_count, srs_params):
    """
    Generate a Groth16 proof given QAP polynomials, witness, and SRS parameters

    Returns:
        tuple: (A_1, B_1, B_2, C_1, psi_points_public) - the proof components and public psi points
    """
    # Unpack SRS parameters
    (g1_points, g2_points, ht_points, alpha_1, beta_1, beta_2,
     delta_1, delta_2, gamma_2, psi_points_public, psi_points_private) = srs_params

    # Multiply QAP polynomials by witness
    l_w = multiply_by_witness(l_polys, witness)
    r_w = multiply_by_witness(r_polys, witness)
    o_w = multiply_by_witness(o_polys, witness)

    # Generate h polynomial
    h = get_h(l_w, r_w, o_w, constraint_count, curve_order, GF(curve_order, primitive_element=5, verify=False))

    # Evaluate QAP on SRS
    l_point = evaluate_list_srs(l_w, g1_points, G1, GF(curve_order, primitive_element=5, verify=False))
    r_point_1 = evaluate_list_srs(r_w, g1_points, G1, GF(curve_order, primitive_element=5, verify=False))
    r_point_2 = evaluate_list_srs(r_w, g2_points, G2, GF(curve_order, primitive_element=5, verify=False))
    o_point = evaluate_list_srs(o_w, g1_points, G1, GF(curve_order, primitive_element=5, verify=False))
    h_point = evaluate_poly_srs(h, ht_points, G1, GF(curve_order, primitive_element=5, verify=False))

    psi_private_point = evaluate_psi_srs_private(public_param_count, witness, psi_points_private, G1)

    # Generate random values
    r = randint(0, curve_order)
    s = randint(0, curve_order)

    # Calculate A_1 = alpha_1 + l_point + r * delta_1
    A_1 = add(
        alpha_1,
        add(
            l_point,
            multiply(delta_1, r)
        )
    )

    # Calculate B_1 = beta_1 + r_point_1 + s * delta_1
    B_1 = add(
        beta_1,
        add(
            r_point_1,
            multiply(delta_1, s)
        )
    )

    # Calculate B_2 = beta_2 + r_point_2 + s * delta_2
    B_2 = add(
        beta_2,
        add(
            r_point_2,
            multiply(delta_2, s)
        )
    )

    # For negative rs
    rs = int(-(GF(curve_order, primitive_element=5, verify=False)(r) * GF(curve_order, primitive_element=5, verify=False)(s)))

    # Calculate salt component = s*A_1 + r*B_1 - rs*del_1
    salt_component_point = add(
        multiply(A_1, s),
        add(
            multiply(B_1, r),
            multiply(delta_1, rs)
        )
    )

    # Calculate C_1 = psi_private_1 + h_point1 + s*A_1 + r*B_1 - rs*delta_1
    C_1 = add(
        psi_private_point,
        add(
            h_point,
            salt_component_point
        )
    )

    return A_1, B_1, B_2, C_1, psi_points_public