import galois
import numpy as np

GF = galois.GF(71)
p_1 = galois.Poly([52, 24, 61], field=GF)
p_2 = galois.Poly([40, 40, 58], field=GF)


poly_added = p_1 + p_2
poly_multiplied = p_1 * p_2

print(poly_added)
print(poly_multiplied)

poly_multiplied_roots = poly_multiplied.roots()
print(poly_multiplied_roots)

roots = [(10, 15), (23, 29)]
f = galois.Poly.Roots(roots, field=GF)
print(f)


# x = GF([236, 87, 38, 112])
# print(x)
# print(GF.properties)
# print(issubclass(GF, galois.FieldArray))
# print(issubclass(GF, np.ndarray))

# y = np.array([109, 17, 108, 224])
# y = y.view(GF)
# print(isinstance(y, galois.FieldArray))

# GF.repr("poly")
# print(x)