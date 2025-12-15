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

def generate_srs(term_nos, mod, GF, G1=G1, G2=G2):
    discrete_log = randint(0, mod)
    # discrete_log = 100
    # G1
    g1_vector = generate_point_vector(discrete_log, term_nos, G1)
    g2_vector = generate_point_vector(discrete_log, term_nos, G2)

    # For h(x) evaluation, we need powers of G1 * Z(s) where s is the secret
    vanishing_poly = get_vanishing_poly(term_nos, mod, GF)
    evaluated_poly = vanishing_poly(discrete_log)
    print("evaluated poly: ", evaluated_poly)
    ht_vector = generate_ht_point_vector(evaluated_poly, g1_vector)
    return (g1_vector, g2_vector, ht_vector)

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
        
