import unittest
import numpy as np
from PIL import Image
from steganography.strategies.compression_strategy import hide_data_in_LSB, hide_compressed_data, get_compressed_data

CARRY_IMAGE_PATH = "../resources/hello.png"
SECRET_IMAGE_PATH = "../resources/basi0g01.png"


class TestCompressionStrategy(unittest.TestCase):

    def test_compression_strategy(self):
        with Image.open(CARRY_IMAGE_PATH) as image:
            image = np.array(image)

        image = image.ravel()

        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()

        image = hide_compressed_data(image, data)
        data = get_compressed_data(image)

        with open(SECRET_IMAGE_PATH, 'rb') as secret:
            secret = secret.read()
        assert(data == secret)