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

def generate_ht_point_vector(evaluated_poly, g1_vector, delta_discrete_log, GF):
    polys = []
    delta_inv = int(GF(1) / GF(delta_discrete_log))
    multiplier = int(evaluated_poly * delta_inv)

    # print("delta: ", delta_discrete_log)
    # print("delta_inv: ", delta_inv)
    # print("evaluated_poly: ", evaluated_poly)
    # print("multiplier: ", multiplier)
    for i in range(len(g1_vector)):
        polys.append(
            multiply(
                g1_vector[i], 
                multiplier
            )
        )

    return polys

def generate_psi_internal(l_poly, r_poly, o_poly, alpha_discrete_log, beta_discrete_log, inv_multiplier, g1_vector, G1, GF):
    l_evaluated = multiply(evaluate_poly_srs(l_poly, g1_vector, G1, GF), beta_discrete_log)
    r_evaluated = multiply(evaluate_poly_srs(r_poly, g1_vector, G1, GF), alpha_discrete_log)
    o_evaluated = evaluate_poly_srs(o_poly, g1_vector, G1, GF)

    psi_i = multiply(
        add(
            l_evaluated,
            add(
                r_evaluated,
                o_evaluated
            ),
        ),
        inv_multiplier
    )

    return psi_i

def generate_psi_points(public_param_nos, alpha_discrete_log, beta_discrete_log, gamma_discrete_log, delta_discrete_log, g1_vector, l_polys, r_polys, o_polys, G1, GF):
    psi_points_public = []
    psi_points_private = []
    gamma_inv = int(GF(1) / GF(gamma_discrete_log))
    delta_inv = int(GF(1) / GF(delta_discrete_log))


    for i in range(public_param_nos):
        psi_points_public.append(
            generate_psi_internal(
                l_polys[i],
                r_polys[i],
                o_polys[i],
                alpha_discrete_log,
                beta_discrete_log,
                gamma_inv,
                g1_vector,
                G1, 
                GF
            )
        )

    for i in range(public_param_nos, len(l_polys)):
        psi_points_private.append(
            generate_psi_internal(
                l_polys[i],
                r_polys[i],
                o_polys[i],
                alpha_discrete_log,
                beta_discrete_log,
                delta_inv,
                g1_vector,
                G1, 
                GF
            )
        )
    return (psi_points_public, psi_points_private)

def generate_srs(term_nos, public_param_nos, mod, l_polys, r_polys, o_polys, GF, G1=G1, G2=G2):
    main_discrete_log = randint(0, mod)
   
    # G1
    g1_vector = generate_point_vector(main_discrete_log, term_nos, G1)
    g2_vector = generate_point_vector(main_discrete_log, term_nos, G2)

    alpha_discrete_log = randint(0, mod)
    beta_discrete_log = randint(0, mod)
    gamma_discrete_log = randint(0, mod)
    delta_discrete_log = randint(0, mod)

    # For h(x) evaluation, we need powers of G1 * Z(s) where s is the secret
    vanishing_poly = get_vanishing_poly(term_nos, mod, GF)
    # print("vanishing_poly: ", vanishing_poly)
    # print("g1 vector: ", g1_vector)
    evaluated_poly = vanishing_poly(main_discrete_log)
    # print("srs: generating ht_vector...")

    ht_vector = generate_ht_point_vector(evaluated_poly, g1_vector, delta_discrete_log, GF)
    # print("ht_vector: ", ht_vector)
    print("srs: ht_vector generated")

    alpha_1 = multiply(G1, alpha_discrete_log)
    beta_1 = multiply(G1, beta_discrete_log)
    beta_2 = multiply(G2, beta_discrete_log)

    print("srs: generating psi points...")
    (psi_points_public, psi_points_private) = generate_psi_points(
        public_param_nos,
        alpha_discrete_log, 
        beta_discrete_log, 
        gamma_discrete_log,
        delta_discrete_log,
        g1_vector,
        l_polys,
        r_polys,
        o_polys,
        G1,
        GF
    )

    delta_1 = multiply(G1, delta_discrete_log)
    delta_2 = multiply(G2, delta_discrete_log)
    gamma_2 = multiply(G2, gamma_discrete_log)
    print("srs: psi points generated")
    return (g1_vector, g2_vector, ht_vector, alpha_1, beta_1, beta_2, delta_1, delta_2, gamma_2, psi_points_public, psi_points_private)

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
        
