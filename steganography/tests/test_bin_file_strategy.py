import unittest
from PIL import Image
from steganography.strategies.bin_file_strategy import bin_file_merge
CARRY_IMAGE_PATH = "../resources/hello.png"
SECRET_IMAGE_PATH = "../resources/basi0g01.png"


class TestBinFileStrategy(unittest.TestCase):

    def test_bin_file_merge(self):
        with Image.open(CARRY_IMAGE_PATH) as image, open(SECRET_IMAGE_PATH, 'rb') as s_bin:
            seed = 0
            pixel_data = bin_file_merge(image, s_bin.read(), seed)
            s_image = Image.fromarray(pixel_data)
            assert(image != s_image)
