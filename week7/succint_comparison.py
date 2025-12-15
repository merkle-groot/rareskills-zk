import numpy as np
from galois import GF, lagrange_poly
from random import randint

prime = 89
GF = GF(prime)

def compute_lagrange(vector, interpolation):
    return lagrange_poly(GF(interpolation), GF(vector))


def compare(matrix_1, matrix_2, mul_vector):
    if matrix_1.shape != matrix_2.shape or matrix_1.shape[1] != mul_vector.shape[0]:
        print("not equal")
        return 0
    
    interpolation_vector = [i+1 for i in range(matrix_1.shape[0])]
    matrix_1_polys = [
        lagrange_poly(GF(interpolation_vector), mul_vector[i] * GF(matrix_1[:, i].flatten().tolist()))
        for i in range(matrix_1.shape[1])
    ]
    matrix_2_polys = [
        lagrange_poly(GF(interpolation_vector), mul_vector[i] * GF(matrix_2[:, i].flatten().tolist()))
        for i in range(matrix_2.shape[1])
    ]

    simplifed_poly_1 = GF(0)
    simplifed_poly_2 = GF(0)
    for i in range(matrix_1.shape[1]):
        simplifed_poly_1 += matrix_1_polys[i]
        simplifed_poly_2 += matrix_2_polys[i]

    evaluation_point = randint(0, prime-1)

    if simplifed_poly_1(evaluation_point) == simplifed_poly_2(evaluation_point):
        print("equal")
        return 1
    else:
        print("not equal")
        return 0


matrix_1 = np.array([[1, 2, 5], [3, 4, 1], [5, 6, 4]])
matrix_2 = np.array([[1, 2, 5], [3, 4, 1], [5, 6, 4]])
mul_vector = np.array([1, 2, 3])
compare(matrix_1, matrix_2, mul_vector)

