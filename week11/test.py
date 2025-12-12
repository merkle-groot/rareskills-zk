from py_ecc.bn128.bn128_pairing import pairing, final_exponentiate
from py_ecc.bn128 import G1, G2, multiply
def E(P, Q):
    return final_exponentiate(pairing(P, Q))

p1 = E(multiply(G2, 5), multiply(G1, 2))
p2 = E(multiply(G2, 5), multiply(G1, 1))
p3 = E(multiply(G2, 3), multiply(G1, 5))
# p4 = E(multiply(G2, 2), multiply(G1, 1))

print(p1 * p2 == p3)            # True
print(p1 * p2.inv() == p2)     # True now
