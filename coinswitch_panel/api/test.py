from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

private_key_hex = "a9362ee30a982b9b6b74961ea63e44120bb73f3b918ba4b0ffe2a8294ff299b4"
public_key_hex  = "c027bfeba58472e04f3d07059bb530d5e9ebb8c55a7b9bc7dd4a13efe7e5c851"

private_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_key_hex))
public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))

message = b"Hello, this is a test"

# Sign using private key
signature = private_key.sign(message)

# Verify using public key
public_key.verify(signature, message)

print("SUCCESS: The key pair works!")
print("Signature:", signature.hex())

# from cryptography.hazmat.primitives.asymmetric import ed25519


# private_key = ed25519.Ed25519PrivateKey.generate()
# public_key = private_key.public_key()

# print("publicKey:", public_key.public_bytes_raw().hex())
# print("secretKey:", private_key.private_bytes_raw().hex())


# from cryptography.hazmat.primitives.asymmetric import ed25519

# # Generate a new Ed25519 private key
# private_key = ed25519.Ed25519PrivateKey.generate()

# # Get the corresponding public key
# public_key = private_key.public_key()

# # Convert both keys to raw bytes and then to hex
# private_key_hex = private_key.private_bytes_raw().hex()
# public_key_hex = public_key.public_bytes_raw().hex()

# print("Mas pub key:", public_key_hex)
# print("Mas pri key:", private_key_hex)