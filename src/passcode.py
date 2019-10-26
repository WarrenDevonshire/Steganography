import binascii

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

backend = default_backend()
passCode = "blah blah blah"

salt = bytes(4)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # 256 bits
    salt=salt,  # salt is 0x0000
    iterations=100000,
    backend=backend
)
key = kdf.derive(passCode.encode())
print(binascii.hexlify(key))

# verify

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)
kdf.verify(passCode.encode(), key)  # will throw if key doesn't match
