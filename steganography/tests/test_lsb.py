import unittest
from PIL import Image
import numpy as np

from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB
from steganography.utilities.aes import generate_key_and_seed, encrypt, decrypt

IMAGE = "../resources/hello.png"
FILE = "../resources/basi0g01.png"
PASSCODE = "Hello, World!"


class TestLsb(unittest.TestCase):

    def test_lsb(self):
        with Image.open(IMAGE) as image, open(FILE, 'rb') as file:
            image = np.array(image).ravel()
            data = file.read()

        data0 = data
        key, seed = generate_key_and_seed(PASSCODE)
        data = encrypt(data, key)

        data = np.frombuffer(data, dtype='uint8')

        data = np.unpackbits(data)

        carry = hide_data_in_LSB(image, data, seed)

        key, seed = generate_key_and_seed(PASSCODE)
        data2 = get_data_in_LSB(carry, seed)

        data2 = data2.tobytes()
        data2 = decrypt(data2, key)

        assert(data0 == data2)
