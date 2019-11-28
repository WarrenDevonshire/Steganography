import unittest
from PIL import Image
import numpy as np

from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB
from steganography.utilities.aes import generate_key_and_seed, encrypt, decrypt
from steganography.utilities.compression import compress_data, decompress_data

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
        print(type(data), data)

        data = np.unpackbits(data)
        # data = np.packbits(data)
        # data = data.tobytes()
        #
        # print(type(data), data)

        carry = hide_data_in_LSB(image, data, seed)

        print("carry:", type(carry), carry)

        key, seed = generate_key_and_seed(PASSCODE)
        data2 = get_data_in_LSB(carry, seed)

        print("data2", type(data2), len(data2), data2)
        data2 = data2.tobytes()
        data2 = decrypt(data2, key)

        print("data0:", type(data0), len(data0), data0)
        print("Decrypt:", type(data2), len(data2), data2)
        assert(data0 == data2)
