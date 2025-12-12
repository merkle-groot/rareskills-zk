from functools import reduce
from py_ecc.bn128 import G1, G2, multiply, add
from random import randint
from py_ecc.bn128 import curve_order

def generate_point_vector(discrete_log, degree, G):
    return [multiply(G, discrete_log**i) for i in range(degree)]

def generate_srs(degree, curve_order=curve_order, G1=G1, G2=G2):
    # discrete_log = randint(0, curve_order)
    discrete_log = 2
    # G1
    g1_vector = generate_point_vector(discrete_log, degree, G1)
    g2_vector = generate_point_vector(discrete_log, degree, G2)

    return (g1_vector, g2_vector)

def evaluate_on_srs(polys, point_vector, degree, G, GF):
    result = multiply(G, 0)
    for poly in polys:
        coeffs = list(reversed(poly.coeffs))
        result = add(result, inner_product_poly_coeffs_point_vector(coeffs, point_vector, degree, G, GF))

    return result

def inner_product_poly_coeffs_point_vector(poly_coeffs, point_vector, degree, G, GF):
    if len(poly_coeffs) != degree:
        diff = degree - len(poly_coeffs)

        for i in range(diff):
            poly_coeffs.append(GF(0))

    print(len(point_vector), len(poly_coeffs))

    result = multiply(G, 0)
    for i in range(degree):
        print("coeff:", poly_coeffs[i], point_vector[i])
        # Convert Galois field element to integer for multiplication
        coeff_int = int(poly_coeffs[i])
        point = multiply(point_vector[i], coeff_int)
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
        
