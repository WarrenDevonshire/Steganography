import unittest
from steganography.core.core import Steganography
from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB

IMAGE = "../resources/hello.png"
DATA = "../resources/basi0g01.png"
OUT_PATH = "../out/test_hide_data.png"
OUT_DATA_PATH = "../out/data.png"
PASSCODE = "Hello, World!"


class TestCore(unittest.TestCase):

    def test_hide_data_with_lsb(self):
        st = Steganography()
        st.set_output_path(path_to_output=OUT_PATH)
        st.hide_data(path_to_carry=IMAGE, path_to_secret=DATA, strategy=hide_data_in_LSB)

    def test_get_data_with_lsb(self):
        st = Steganography()
        st.set_output_path(path_to_output=OUT_DATA_PATH)
        st.get_data(path_to_carry=OUT_PATH, strategy=get_data_in_LSB)
