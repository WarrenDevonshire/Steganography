from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64


def encrypt(data, key):
    f = Fernet(key)
    data = f.encrypt(data)
    return data


def decrypt(token, key):
    f = Fernet(key)
    return f.decrypt(token)


def generate_key_and_seed(passcode):
    passcode = str.encode(passcode)
    salt = bytes(4)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=36,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = kdf.derive(passcode)
    seed = int.from_bytes(key[32:], byteorder='big')
    return base64.urlsafe_b64encode(key[:32]), seed
