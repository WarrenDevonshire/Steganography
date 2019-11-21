import binascii
import unittest
from steganography.utilities.identify import type_of_file, type_of_bin

PNG_HEADER_SIG = binascii.hexlify(b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a")


class TestIdentify(unittest.TestCase):

    def test_type_of_file(self):
        b = type_of_file("../resources/hidden.png")
        assert(b is True)

    def test_type_of_bin(self):
        buffer = int(PNG_HEADER_SIG, 16).to_bytes(length=8, byteorder='big', signed=False)
        type_of_bin(buffer)
