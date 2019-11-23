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

        d_token = decrypt(token, key)

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
        token = np.frombuffer(token, 'uint8')
        print(len(token), token)
        token = np.unpackbits(token)
        print(len(token), token)
