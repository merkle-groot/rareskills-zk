from galois import GF, lagrange_poly
import numpy as np

def interpolate(points, vector):
    return lagrange_poly(GF(points), GF(vector))

# addition
p = 89
GF = GF(p)

v1 = np.array([1, 4, 9])
v2 = np.array([1, 8, 27])
v12 = v1 + v2


interpolation_points = np.array([1, 2, 3])
p1 = interpolate(interpolation_points, v1)
p2 = interpolate(interpolation_points, v2)
p12 = interpolate(interpolation_points, v12)

assert p1 + p2 == p12

# scalar multiplication
v3 = np.array([3, 6, 11])
v3_multiplied = np.array([x*21 % p for x in v3])
scalar = GF(21)

p3 = scalar * interpolate(interpolation_points, v3)
p3_multiplied = interpolate(interpolation_points, v3_multiplied)

assert p3 == p3_multiplied
