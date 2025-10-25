from galois import GF, lagrange_poly
import numpy as np
from random import randint

prime = 89
GF = GF(prime)

def check_equality(vec_1, vec_2):
    if len(vec_1) != len(vec_2):
        print("not equal")
        return 0
    
    interpolation_points = [randint(0, prime-1) for x in range(len(vec_1))]

    vec_1_poly = lagrange_poly(GF(interpolation_points), GF(vec_1))
    vec_2_poly = lagrange_poly(GF(interpolation_points), GF(vec_2))

    evaluation_point = randint(0, prime-1)

    if vec_1_poly(evaluation_point) == vec_2_poly(evaluation_point):
        print("equal")
        return 1
    else:
        print("not equal")
        return 0

x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 6]
check_equality(x, y)