from utils import add, sub, multiply, get_modulus, get_inverse

class Matrix:
    def __init__(self, a, b, c, d):
        self.matrix = [[get_modulus(a), get_modulus(b)], [get_modulus(c), get_modulus(d)]]

    def determinant(self):
        [[a, b], [c, d]] = self.matrix
        return sub(multiply(a, d), multiply(b, c))

    def inverse(self):
        [[a, b], [c, d]] = self.matrix
        inverted = [
            [d, get_modulus(-b)], 
            [get_modulus(-c), a]
        ]
        det_inv = get_inverse(self.determinant())
        return [[get_modulus(x * det_inv) for x in row] for row in inverted]

    def matrix_mult(self, matrix1):
        [[a, b], [c, d]] = self.matrix
        [[e, f], [g, h]] = matrix1

        return [
            [
                add(multiply(a, e), multiply(c, g)), 
                add(multiply(a, f), multiply(c, h)),
            ], 
            [
                add(multiply(b, e), multiply(d, g)),
                add(multiply(b, f), multiply(d, h)), 
            ]
        ]



    

    