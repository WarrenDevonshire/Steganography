import unittest
from steganography.strategies.bin_strategy import random_merge, random_retrieve
from steganography.utilities.hash import get_seed
from PIL import Image
CARRY_IMAGE_PATH = "../resources/hello.png"
SECRET_IMAGE_PATH = "../resources/basi0g01.png"


class TestBinStrategy(unittest.TestCase):

    def test_strategy(self):
        with Image.open(SECRET_IMAGE_PATH) as s_image:
            seed = get_seed(pass_code="hello hello hello", salt=bytes(4))
            image = random_merge(CARRY_IMAGE_PATH, SECRET_IMAGE_PATH, seed)
            image = random_retrieve(image, seed)
            assert(s_image == image)
