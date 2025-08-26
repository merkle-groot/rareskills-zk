# Find the elements that are congruent to a = 2/3, b = 1/2, and c = 1/3.
# Verify your answer by checking that a * b = c (in the finite field)

from utils import add, multiply, get_inverse, get_modulus

a = multiply(2, get_inverse(3))
b = multiply(1, get_inverse(2))
c = multiply(1, get_inverse(3))

print("a = ", a)
print("b = ", b)
print("c = ", c)

print("is a * b = c? ", multiply(a, b) == c)