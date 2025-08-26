# What is the modular square root of 12?
# Verify your answer by checking that x * x = 12 (mod 71)
from utils import get_modulus, multiply

ans = -1
for i in range(71):
    if multiply(i, i) == 12:
        ans = i
        break

if ans == -1:
    print("No square root for 12 in field 71?")
else:
    print("The square root for 12 in field 71: ", ans)
    print("Is {ans}*{ans} under mod 71 = 12? ", multiply(ans, ans) == 12)