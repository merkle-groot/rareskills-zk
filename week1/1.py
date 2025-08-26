# Find the elements in a finite field that are congruent to the following values:
# -1
# -4
# -160
# 500

from utils import get_modulus

print("-1 = ", get_modulus(-1))
print("-4 =", get_modulus(-4))
print("-160 =", get_modulus(-160))
print("500 = ", get_modulus(500))

