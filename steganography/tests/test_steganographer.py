import unittest
from steganography.core.Steganographer import Steganographer
from steganography.strategies.lsb import hide_data_in_LSB

IMAGE = "../resources/hello.png"
DATA = "../resources/basi0g01.png"
OUT_PATH = "../out/hidden_data.png"
PASSCODE = "Hello, World!"


class TestSteganographer(unittest.TestCase):

    def test_hide_data_from_file(self):
        st = Steganographer(IMAGE)
        st.hide_data_from_file(DATA, OUT_PATH, hide_data_in_LSB, PASSCODE)

        with open(IMAGE, 'rb') as image, open(OUT_PATH, 'rb') as output:
            image = image.read()
            output = output.read()

        assert(image != output)
