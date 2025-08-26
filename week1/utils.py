p = 71

def get_modulus(num):
    return num % p

def get_inverse(num):
    return pow(num, -1, p)

def add(num1, num2):
    return (num1 + num2) % p

def sub(num1, num2):
    return (num1 - num2) % p

def multiply(num1, num2):
    return (num1 * num2) % p


