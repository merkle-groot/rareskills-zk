# Compute the inverse of the following matrix in the finite field:
# [1, 1, 1, 4]
# Verify your answer by checking that A*A^1 = I

from matrix_utils import Matrix

def get_identity_matrix():
    return [[1, 0], [0, 1]]

m = Matrix(1, 1, 1, 4)
print("determinant: ", m.determinant())
print("inverse of m: ", m.inverse())
print("A*A^-1? ", m.matrix_mult(m.inverse()) == get_identity_matrix())