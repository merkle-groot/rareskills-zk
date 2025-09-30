import sys
from py_ecc.bn128 import G2, multiply
from eth_abi import encode

scalar = int(sys.argv[1])
result = multiply(G2, scalar)

types = ['uint', 'uint', 'uint', 'uint']
values = [  int(result[0].coeffs[0]),
            int(result[0].coeffs[1]),
            int(result[1].coeffs[0]),
            int(result[1].coeffs[1])
]
encoded = encode(types, values)
print(encoded.hex())  # Hex representation
