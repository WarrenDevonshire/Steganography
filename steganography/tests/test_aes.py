import base64
import unittest
from steganography.utilities.aes import encrypt, decrypt, generate_key_and_seed
import numpy as np

SECRET_IMAGE_PATH = "../resources/basi0g01.png"


class TestAES(unittest.TestCase):

    def test_encrypt(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
        key, seed = generate_key_and_seed("Hello, World!")

        token = encrypt(data, key)

        token += data
        token += data
        token += data
        token += data
        token += b"hello world!dfasfdafdsafdsafdsafdsafdsafdsafdsafdsafdsa"

        d_token = decrypt(token, key)

        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()

        print(data)
        print(token)
        print(d_token)
        assert(data == d_token)

    def test_generate_key(self):
        password = "Hello, World!"
        key, seed = generate_key_and_seed(password)
        assert(len(key) == 44)
        assert(seed < 2**32 - 1)

    def test_token_iteration(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
        key, seed = generate_key_and_seed("hello")

        token = encrypt(data, key)

        print("Encrypt:", type(token), token)
        base64.urlsafe_b64decode(token)
        print("Decode:", type(token), token)
        token = np.frombuffer(token, 'uint8')
        print("np:", type(token), token)

        token = np.unpackbits(token)
        for i in range(0, 100):
            np.append(token, i % 2)
        token = np.packbits(token)
        token = token.tobytes()
        for i in range(0, 5):
            token += int(2**32 - 1).to_bytes(50_000, byteorder='big')
        token = int(2**32 - 1).to_bytes(8, byteorder='big') + token

        data = decrypt(token, key)

        print(data)



