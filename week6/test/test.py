from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq, curve_order, neg, field_modulus

assert eq(add(multiply(G1, curve_order), multiply(G1, 5)), multiply(G1, 5))
assert eq(add(multiply(G2, curve_order), multiply(G2, 5)), multiply(G2, 5))

p1 = neg(multiply(G1, 2))
# print(p1)
p2 =  multiply(G2, 6)
# print(p2)

p3 = multiply(G1, 4)
# 
p4 = multiply(G2, 3)
# assert eq(pairing(p2, p1), pairing(p4, p3))

# print(pairing(p2, p1) * pairing(p4, p3))

# print(curve_order)
# powfield = field_modulus**12 - 1
# print(powfield)
# print(powfield % curve_order)