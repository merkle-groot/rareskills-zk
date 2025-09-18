from ecpy.curves import Curve
import random
import hashlib

# key init
cv   = Curve.get_curve('secp256k1')
private_key = random.randint(1, cv.order - 1)
public_key = private_key * cv.generator
print(f"priv key: {private_key}, pub key: {public_key}")

# message to sign
message = "secret message"
message_hash = hashlib.sha256(message.encode()).hexdigest()
message_hash_int = int('0x' + message_hash, 16)
print(f"message: {message}, it's hash: {message_hash}")

# sign message
# get a random EC point and it's multiplier
random_multiplier = random.randint(1, cv.order - 1)
random_point = random_multiplier * cv.generator
random_point_x = random_point.x
random_multiplier_inverse = pow(random_multiplier, -1, cv.order)
print(f"""point multiplier: {random_multiplier}, point: {random_point}, x: {random_point_x}, 
    inverse multiplier: {random_multiplier_inverse}""")

signed_message = random_multiplier_inverse * (message_hash_int + random_point_x * private_key)
print(f"r: {random_multiplier}, s: {signed_message}")


# ec recover
signed_message_inverse = pow(signed_message, -1, cv.order)
recovered_point = (signed_message_inverse * message_hash_int) * cv.generator + (signed_message_inverse * random_point_x) * public_key
assert recovered_point.x == random_point_x