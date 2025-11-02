from galois import GF, lagrange_poly, Poly
import numpy as np

prime = 79
GF = GF(prime)

def get_poly(vec):
    xs = [1, 2, 3]
    return lagrange_poly(GF(xs), GF(vec))

def sanitize_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] = m[i][j] % prime

    return np.array(m)

L = sanitize_matrix(
        [
            [0,0,3,0,0,0],
            [0,0,0,0,1,0],
            [0,0,1,0,0,0]
        ]
    )

R = sanitize_matrix(
        [
            [0,0,1,0,0,0],
            [0,0,0,1,0,0],
            [0,0,0,5,0,0]
        ]
    )

O = sanitize_matrix(
        [
            [0,0,0,0,1,0],
            [0,0,0,0,0,1],
            [-3,1,1,2,0,-1]
        ]
    )

l_polys = []
r_polys = []
o_polys = []

w = np.array([x % prime for x in [1, 3049703, 100, 100, 30000, 3000000]])

for i in range(L.shape[1]):
    l_polys.append(get_poly(L[:, i]) * GF(w[i]))
    r_polys.append(get_poly(R[:, i]) * GF(w[i]))
    o_polys.append(get_poly(O[:, i]) * GF(w[i]))

l = l_polys[0]
for poly in l_polys[1:]:
    l += poly

r = r_polys[0]
for poly in r_polys[1:]:
    r += poly

o = o_polys[0]
for poly in o_polys[1:]:
    o += poly

l_r = l * r

# they are equal at interpolating points
assert (l_r)(1) == o(1)
assert (l_r)(2) == o(2)
assert (l_r)(3) == o(3)

# they differ at every other points
assert (l_r)(24) != o(24)
assert (l_r)(65) != o(65)

# calculate a polynomial with zeroes at 1, 2 and 3
p1 = Poly([1, (-1) % prime], field=GF) 
p2 = Poly([1, (-2) % prime], field=GF)  
p3 = Poly([1, (-3) % prime], field=GF)  #
t = p1 * p2 * p3

# calculate h, where h*t gives zeroes at 1, 2 and 3, makes rhs equal to lhs
h = (l_r - o)//t

# verify the division is correct
assert (l_r - o) == h * t

lhs = l_r
rhs = o + h*t

print(f"lhs: {lhs}")
print(f"rhs: {rhs}")
print(f"h: {h}")
print(f"t: {t}")

# check if polynomials are equal
assert lhs == rhs
assert (lhs)(1) == rhs(1)
assert (lhs)(2) == rhs(2)
assert (lhs)(3) == rhs(3)
assert (lhs)(4) == rhs(4)
assert (lhs)(5) == rhs(5)