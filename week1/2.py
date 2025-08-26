# Find the elements that are congruent to a = 5/6, b = 11/12, and c = 21/12
# Verify your answer by checking that a + b = c (in the finite field)

from utils import add, multiply, get_inverse, get_modulus

a = multiply(5, get_inverse(6))
b = multiply(11, get_inverse(12))
c = multiply(21, get_inverse(12))

print("a = ", a)
print("b = ", b)
print("c = ", c)

print("is a + b = c? ", add(a, b) == c)

