import binascii

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def get_seed(pass_code, salt):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits
        salt=salt,  # salt is 0x0000
        iterations=100000,
        backend=backend
    )
    return int(binascii.hexlify(kdf.derive(pass_code.encode())), 16)
