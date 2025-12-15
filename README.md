# RareSkills Zero-Knowledge Bootcamp

This repository contains all coding assignments and projects completed during the RareSkills Zero-Knowledge Proof Bootcamp. 

### Weekly Assignments
- **[week1/](week1/)** - Introduction to finite fields and modular arithmetic
- **[week2/](week2/)** - ECDSA algo
- **[week5/](week5/)** - Working with fields and matrices in Solidity
- **[week6/](week6/)** - Pairings in Solidity 
- **[week7/](week7/)** - Rank-1 Constraint Systems (R1CS)
- **[week8/](week8/)** - Schwartz Zippel Lemma & Lagrange interpolation hands-on
- **[week9/](week9/)** - QAP hands-on
- **[week10/](week10/)** - QAP evaluation on SRS
- **[week11/](week11/)** - Groth16 part1
- **[groth16/](groth16/)** - Groth16 complete

### Main Project: Groth16 Implementation
The capstone project is a complete Python implementation of the Groth16 zk-SNARK protocol:

#### **[groth16/](groth16/)**
- **Complete Groth16 protocol implementation** from scratch
- Trusted setup with Structured Reference String (SRS)
- Proving and verification systems
- Example arithmetic circuits

Key features:
- Uses BN128 elliptic curve (`py_ecc`)
- Finite field arithmetic with `galois`
- R1CS to QAP transformation
- Polynomial operations and Lagrange interpolation

```bash
cd groth16
python main.py
```

## Technologies Used

- **Python 3** - Primary implementation language
- **py_ecc** - Elliptic curve cryptography (BN128)
- **galois** - Finite field arithmetic and polynomial operations
- **NumPy** - Matrix operations

## Getting Started

Each week folder contains independent exercises that can be run individually. For the complete Groth16 implementation:

1. Install dependencies:
   ```bash
   pip install py_ecc galois numpy
   ```

2. Run the main example:
   ```bash
   cd groth16
   python main.py
   ```