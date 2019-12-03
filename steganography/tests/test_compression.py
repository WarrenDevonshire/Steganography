import unittest
from steganography.utilities.compression import compress_data, decompress_data
CARRY_IMAGE_PATH = "../resources/hello.png"
SECRET_IMAGE_PATH = "../resources/basi0g01.png"


class TestCompression(unittest.TestCase):

    def test_compress_file(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
            compressed_data = compress_data(data)

    def test_decompress_file(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
            compressed_data = compress_data(data)
            decompressed_data = decompress_data(compressed_data)

            assert(data == decompressed_data)

    def test_decompress_file_with_added_data(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
            compressed_data = compress_data(data)
            compressed_data += data

            decompressed_data = decompress_data(compressed_data)

            assert(data == decompressed_data)

    def test_byte_loop(self):
        with open(SECRET_IMAGE_PATH, 'rb') as file:
            data = file.read()
            b_arr = ''
            for byte in data:
                byte = '{0:08b}'.format(byte)
                for bit in byte:
                    b_arr += bit
            r_data = int(b_arr, 2).to_bytes(length=len(data), byteorder='big', signed=False)
