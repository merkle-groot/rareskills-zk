import sys
from py_ecc.bn128 import G1, multiply
from eth_abi import encode

scalar = int(sys.argv[1])
result = multiply(G1, scalar)

types = ['uint', 'uint']
values = [  
    int(result[0]),
    int(result[1])
]
encoded = encode(types, values)
print(encoded.hex())