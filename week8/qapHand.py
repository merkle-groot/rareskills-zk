from scipy.interpolate import lagrange
import numpy as np

def get_poly(vec):
    xs = [1, 2, 3]
    return lagrange(xs, vec)

L = np.array([
        [0,0,3,0,0,0],
        [0,0,0,0,1,0],
        [0,0,1,0,0,0]
    ])

R = np.array([
        [0,0,1,0,0,0],
        [0,0,0,1,0,0],
        [0,0,0,5,0,0]
    ])

O = np.array([
        [0,0,0,0,1,0],
        [0,0,0,0,0,1],
        [-3,1,1,2,0,-1]
    ])

l_polys = []
r_polys = []
o_polys = []
w = np.array([1, 3049703, 100, 100, 30000, 3000000])
for i in range(L.shape[1]):
    l_polys.append(get_poly(L[:, i]) * w[i])
    r_polys.append(get_poly(R[:, i]) * w[i])
    o_polys.append(get_poly(O[:, i]) * w[i])

l = sum(l_polys)
r = sum(r_polys)
o = sum(o_polys)

l_r = l * r

# they are equal at interpolating points
assert (l_r)(1) == o(1)
assert (l_r)(2) == o(2)
assert (l_r)(3) == o(3)

# they differ at every other points
assert (l_r)(24) != o(24)
assert (l_r)(65) != o(65)


# calculate a vector with zeroes at 1, 2 and 3
p1 = np.poly1d([1, -1])
p2 = np.poly1d([1, -2])
p3 = np.poly1d([1, -3])
t = np.polymul(np.polymul(p1, p2), p3)

# calculate h, where h*t is gives zeroes at 1, 2 and 3, makes rhs equal to lhs
h, r = (l_r - o)/t


lhs = l_r
rhs = o + h*t

assert lhs == rhs
assert (lhs)(1) == rhs(1)
assert (lhs)(2) == rhs(2)
assert (lhs)(3) == rhs(3)
assert (lhs)(4) == rhs(4)
assert (lhs)(5) == rhs(5)