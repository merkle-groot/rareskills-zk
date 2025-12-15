from py_ecc.bn128 import G1, G2, multiply, add
from functools import reduce

def generate_point_vector(n, discrete_log, G):
    return [multiply(G, discrete_log ** i) for i in range(0, n)]

def inner_product_poly_coeffs_point_vector(poly_coeffs, point_vector):
    return reduce(add, map(multiply, point_vector, poly_coeffs))


if __name__ == "__main__":
    n = 3
    discrete_log = 5
    g1_points = generate_point_vector(n, discrete_log, G1)
    g2_points = generate_point_vector(n, discrete_log, G2)

    coeffs = [1, 7, 2]
    print(inner_product_poly_coeffs_point_vector(coeffs, g1_points))


