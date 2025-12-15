from py_ecc.bn128 import curve_order, G1, G2, pairing, multiply, add, neg, eq
from galois import GF


def evaluate_psi_srs(witness, psi_points, G):
    """Evaluate psi SRS points"""
    result = multiply(G, 0)
    for i in range(len(psi_points)):
        result = add(result, multiply(psi_points[i], witness[i]))

    return result


def verify_proof(proof, public_inputs, public_param_count, srs_params):
    """
    Verify a Groth16 proof

    Args:
        proof: tuple (A_1, B_1, B_2, C_1) - the proof components
        public_inputs: witness values including public inputs
        public_param_count: number of public parameters
        srs_params: SRS parameters needed for verification

    Returns:
        bool: True if proof is valid, False otherwise
    """
    A_1, B_1, B_2, C_1, psi_points_public = proof

    # Extract needed SRS parameters for verification
    (g1_points, g2_points, ht_points, alpha_1, beta_1, beta_2,
     delta_1, delta_2, gamma_2, psi_points_public_from_srs, psi_points_private) = srs_params

    # Use the psi_points_public from the proof (they should match SRS)
    psi_points_public = psi_points_public

    # Evaluate � SRS for public witness values
    psi_public_point = evaluate_psi_srs(public_inputs[:public_param_count], psi_points_public, G1)

    # Perform pairings
    pairing_1 = pairing(B_2, neg(A_1))
    pairing_2 = pairing(beta_2, alpha_1)
    pairing_3 = pairing(gamma_2, psi_public_point)
    pairing_4 = pairing(delta_2, C_1)

    # Calculate result
    result = pairing_1 * pairing_2 * pairing_3 * pairing_4
    expected_result = pairing(G2, multiply(G1, 0))

    return eq(result, expected_result)