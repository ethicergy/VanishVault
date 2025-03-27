import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Generate a secure key (256-bit for AES-256)
def generate_key():
    key = AESGCM.generate_key(bit_length=256)
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the key from file
def load_key():
    return open("secret.key", "rb").read()

# Encrypt data using AES-256-GCM
def encrypt_data(data: bytes) -> bytes:
    key = load_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # AES-GCM requires a 12-byte nonce
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    return base64.b64encode(nonce + encrypted_data)  # Store nonce with ciphertext

# Decrypt data using AES-256-GCM
def decrypt_data(encrypted_data: bytes) -> bytes:
    key = load_key()
    aesgcm = AESGCM(key)
    encrypted_data = base64.b64decode(encrypted_data)
    nonce, ciphertext = encrypted_data[:12], encrypted_data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)
