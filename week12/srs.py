from py_ecc.bn128 import G1, G2, multiply, add
from random import randint
from galois import GF, Poly

def generate_point_vector(discrete_log, term_nos, G):
    return [multiply(G, discrete_log**i) for i in range(term_nos)]

def get_vanishing_poly(term_nos, mod, GF):
    vanishing_poly = Poly([1], field=GF)
    for i in range(1, term_nos+1):
        vanishing_poly = vanishing_poly*Poly([1, (-i) % mod], field=GF)
        # print("i: ", Poly([1, (-i) % mod], field=GF), curve_order)
    return vanishing_poly

def generate_ht_point_vector(evaluated_poly, g1_vector):
    polys = []
    for i in range(len(g1_vector)):
        polys.append(multiply(g1_vector[i], int(evaluated_poly)))

    return polys

def generate_psi_points(alpha_discrete_log, beta_discrete_log, g1_vector, l_polys, r_polys, o_polys, G1, GF):
    psi_points = []

    for i in range(len(l_polys)):
        l_evaluated = multiply(evaluate_poly_srs(l_polys[i], g1_vector, G1, GF), beta_discrete_log)
        r_evaluated = multiply(evaluate_poly_srs(r_polys[i], g1_vector, G1, GF), alpha_discrete_log)
        o_evaluated = evaluate_poly_srs(o_polys[i], g1_vector, G1, GF)

        psi_i = add(
            l_evaluated,
            add(
                r_evaluated,
                o_evaluated
            )
        )

        # print(f"l_evaluated at {i}: {l_evaluated}")
        # print(f"r_evaluated at {i}: {r_evaluated}")
        # print(f"o_evaluated at {i}: {o_evaluated}")
        # print(f"psi_i at {i}: {psi_i}")

        psi_points.append(psi_i)

    return psi_points

def generate_srs(term_nos, mod, l_polys, r_polys, o_polys, GF, G1=G1, G2=G2):
    main_discrete_log = randint(0, mod)
    # discrete_log = 100
    # G1
    g1_vector = generate_point_vector(main_discrete_log, term_nos, G1)
    g2_vector = generate_point_vector(main_discrete_log, term_nos, G2)

    alpha_discrete_log = randint(0, mod)
    beta_discrete_log = randint(0, mod)

    # For h(x) evaluation, we need powers of G1 * Z(s) where s is the secret
    vanishing_poly = get_vanishing_poly(term_nos, mod, GF)
    evaluated_poly = vanishing_poly(main_discrete_log)
    print("evaluated poly: ", evaluated_poly)
    ht_vector = generate_ht_point_vector(evaluated_poly, g1_vector)

    alpha = multiply(G1, alpha_discrete_log)
    beta = multiply(G2, beta_discrete_log)

    psi_points = generate_psi_points(
        alpha_discrete_log, 
        beta_discrete_log, 
        g1_vector,
        l_polys,
        r_polys,
        o_polys,
        G1,
        GF
    )
    return (g1_vector, g2_vector, ht_vector, alpha, beta, psi_points)

def evaluate_list_srs(polys, point_vector, G, GF):
    result = multiply(G, 0)
    for poly in polys:
        result = add(result, evaluate_poly_srs(poly, point_vector, G, GF))

    return result

def evaluate_poly_srs(poly, point_vector, G, GF):
    result = multiply(G, 0)
    coeffs = list(reversed(poly.coeffs))
    result = add(result, inner_product_poly_coeffs_point_vector(coeffs, point_vector, G))

    return result

def inner_product_poly_coeffs_point_vector(poly_coeffs, point_vector, G):
    result = multiply(G, 0)
    for i in range(len(poly_coeffs)):
        # Convert Galois field element to integer for multiplication
        coeff_int = int(poly_coeffs[i])

        # Skip if coefficient is 0 - multiply returns None which causes issues
        if coeff_int == 0:
            continue

        point = multiply(point_vector[i], coeff_int)

        # Handle case where result might be None (point at infinity)
        if result is None:
            result = point
        else:
            result = add(result, point)
    return result

if __name__ == "__main__":
    g = G1
    discrete_log = 12
    degree = 10

    point_vector = generate_point_vector(discrete_log, degree, g)
    poly_coeffs = [i for i in range(1, degree+1)]
    # poly_coeffs)
    print(inner_product_poly_coeffs_point_vector(poly_coeffs, point_vector))
        
