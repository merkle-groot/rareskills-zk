import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'circuit'))

from src.srs import generate_srs
from py_ecc.bn128 import curve_order, G1, G2
from galois import GF
from src.r1cs import get_qap, sanitize_matrix, check_input
from circuit.circuit import L, R, O, w, public_param_count
from src.prover import generate_proof
from src.verifier import verify_proof


def setup_srs(L, R, O, public_param_count, curve_order):
    """Perform the trusted setup to generate SRS parameters"""
    gf = GF(curve_order, primitive_element=5, verify=False)

    # initial setup, r1cs, qap
    (l_polys, r_polys, o_polys) = get_qap(L, R, O, gf, curve_order)

    # Trusted setup
    constraint_count = len(L)
    term_nos = len(l_polys)

    print("no of constraints: ", constraint_count)
    print("no of signals: ", term_nos)

    srs_params = generate_srs(
        constraint_count,
        public_param_count,
        curve_order,
        l_polys,
        r_polys,
        o_polys,
        gf,
        G1,
        G2
    )

    return l_polys, r_polys, o_polys, constraint_count, srs_params


if __name__ == "__main__":
    # Sanitize witness and check inputs
    w = sanitize_matrix(w, curve_order)
    check_input(L, R, O, w)

    # Setup SRS
    l_polys, r_polys, o_polys, constraint_count, srs_params = setup_srs(
        L, R, O, public_param_count, curve_order
    )

    # Generate proof
    print("Generating proof...")
    proof = generate_proof(
        l_polys, r_polys, o_polys, w, public_param_count,
        constraint_count, srs_params
    )

    # Verify proof
    print("Verifying proof...")
    is_valid = verify_proof(proof, w, public_param_count, srs_params)

    if is_valid:
        print("Proof successful!")
    else:
        print("Proof verification failed!")

    