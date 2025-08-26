import galois
import numpy as np

GF = galois.GF(71)
x = GF([0, 1, 2])
y = GF([1, 2, 1])

poly = galois.lagrange_poly(x, y)
print(poly)

assert poly(0) == 1
assert poly(1) == 2
assert poly(2) == 1