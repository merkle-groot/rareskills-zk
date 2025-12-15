import sys
from py_ecc.bn128 import G1, multiply, curve_order
from eth_abi import encode

scalar = int(sys.argv[1])
if scalar < 0:
    scalar = curve_order + scalar
result = multiply(G1, scalar)

types = ['uint', 'uint']
values = [  
    int(result[0]),
    int(result[1])
]

# print(result)
encoded = encode(types, values)
print(encoded.hex())