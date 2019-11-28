import unittest
from steganography.core.Steganographer import Steganographer
from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB
import logging
IMAGE = "../resources/hello.png"
DATA = "../resources/basi0g01.png"
OUT_PATH = "../out/hidden_data.png"
OUT_DATA_PATH = "../out/data.png"
PASSCODE = "Hello, World!"


class TestSteganographer(unittest.TestCase):

    def test_hide_data_from_file(self):
        logging.basicConfig(filename='TestSteganographerHideData.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')
        st = Steganographer(IMAGE)
        st.hide_data_from_file(DATA, OUT_PATH, hide_data_in_LSB, PASSCODE)

        with open(IMAGE, 'rb') as image, open(OUT_PATH, 'rb') as output:
            image = image.read()
            output = output.read()

        assert(image != output)

    def test_get_data_from_image(self):
        logging.basicConfig(filename='TestSteganographerGetData.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')
        Steganographer.get_data_from_image(OUT_PATH, OUT_DATA_PATH, get_data_in_LSB, PASSCODE)

# Why don't I reverse the retrieval?
# I need a header for data size.
