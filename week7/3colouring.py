import numpy as np

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


print(outputMul)
print(LRMul)

result = outputMul == LRMul
assert result.all()
# print(leftMul)
# print(rightMul)

