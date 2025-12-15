# Groth16 Zero-Knowledge Proof Implementation

This repository contains a Python implementation of the Groth16 zk-SNARK protocol.

## Usage

To run the main example:

```bash
cd groth16
python main.py
```

This will:
1. Load the circuit definition from `circuit/circuit.py`
2. Convert R1CS to QAP using `src/r1cs.py`
3. Generate Structured Reference String using `src/srs.py`
4. Create a proof using `src/prover.py`
5. Verify the proof using `src/verifier.py`

## Dependencies

- `py_ecc` - Elliptic curve cryptography (BN128 curve)
- `galois` - Finite field arithmetic and polynomial operations
- `numpy` - Matrix operations

## Circuit Example

The default circuit in `circuit/circuit.py` demonstrates a simple arithmetic circuit:
- 3 constraints
- 6 signals (3 public, 3 private)
- Demonstrates basic multiplication and addition operations