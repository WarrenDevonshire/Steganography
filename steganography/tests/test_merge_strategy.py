import unittest
from PIL import Image
from steganography.utilities.hash import get_seed
from steganography.strategies.merge_strategy import merge_images, extract_hidden_image
CARRY_IMAGE_FILE = "../resources/canyon1.png"
MESG_IMAGE_FILE = "../resources/hello.png"
MERGED_IMAGE_FILE = "../resources/merged.png"


class TestMergeStrategy(unittest.TestCase):

    def test_strategy(self):
        with Image.open(MESG_IMAGE_FILE) as s_image:
            secretKey = get_seed(pass_code="blah blah blah", salt=bytes(4))

            merged_image = merge_images(CARRY_IMAGE_FILE, MESG_IMAGE_FILE, secretKey)

            hidden_image = extract_hidden_image(MERGED_IMAGE_FILE, MESG_IMAGE_FILE, secretKey)
            assert(s_image == hidden_image)
