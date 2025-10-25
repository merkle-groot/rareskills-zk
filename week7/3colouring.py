import numpy as np
from py_ecc.bn128 import G1, G2, multiply, pairing

# x*x = r
# r*x = 6*r - 11*x + 6
# y*y = s
# s*y = 6*s - 11*y +6
# x*y = t
# t*t = w
# w*t = 11*w -36*t + 36

L = np.matrix([
#   [1, w, t, s, r, x, y]
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
]);

R = np.matrix([
#   [1, w, t, s, r, x, y]
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
]);

O = np.matrix([
#   [1, w, t, s, r, x, y]
    [0, 0, 0, 0, 1, 0, 0],
    [6, 0, 0, 0, 6, -11, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [6, 0, 0, 6, 0, 0, -11],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [36, 11, -36, 0, 0, 0, 0],
]);

x = 1
y = 2
r = x*x
s = y*y
t = x*y
w = t*t

w = np.array([1, w, t, s, r, x, y]);

outputMul = np.matmul(O, w)
leftMul = np.matmul(L, w)
rightMul = np.matmul(R, w)
LRMul = np.multiply(leftMul, rightMul)

result = outputMul == LRMul
assert result.all()

outputMulGt = []
for x in np.array(outputMul[0]).flatten():
    outputMulGt.append(pairing(multiply(G2, x), multiply(G1, 1)))

leftMulMulG2 = []
for x in np.array(leftMul[0]).flatten():
    leftMulMulG2.append(multiply(G2, x))

rightMulG1 = []
for x in np.array(rightMul[0]).flatten():
    rightMulG1.append(multiply(G1, x))

pairingLeftRight = []
for (x, y) in zip(leftMulMulG2, rightMulG1):
    pairingLeftRight.append(pairing(x, y))

for (x, y) in zip(outputMulGt, pairingLeftRight):
    if x == y:
        continue
    else:
        print("not equal")
        break


