import unittest
import numpy as np

CARRY_IMAGE_PATH = "../resources/hello.png"
SECRET_IMAGE_PATH = "../resources/basi0g01.png"


class TestCompressionStrategy(unittest.TestCase):

    def test_numpy_to_bits(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
            byte_array = np.frombuffer(data, dtype='uint8')
            data_str = []
            for byte in data:
                data_str.append(byte)
            print(data_str)
            print(byte_array)

            bits = np.unpackbits(byte_array)
            print(np.packbits(bits))
