import unittest
from PIL import Image
import numpy as np
import logging

from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB
from steganography.utilities.aes import generate_key_and_seed, encrypt, decrypt

IMAGE = "../resources/hello.png"
FILE = "../resources/basi0g01.png"
PASSCODE = "Hello, World!"


def setup_logger():
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


class TestLsb(unittest.TestCase):

    def test_lsb(self):
        setup_logger()
        log = logging.getLogger(__name__)
        log.debug('test_lsb() has started!')
        with Image.open(IMAGE) as image, open(FILE, 'rb') as file:
            image = np.array(image).ravel()
            data = file.read()

        data0 = data
        key, seed = generate_key_and_seed(PASSCODE)
        data = encrypt(data, key)

        data = np.frombuffer(data, dtype='uint8')

        data = np.unpackbits(data)

        carry = hide_data_in_LSB(image, data, seed)

        key, seed = generate_key_and_seed(PASSCODE)
        data2 = get_data_in_LSB(carry, seed)

        data2 = data2.tobytes()
        data2 = decrypt(data2, key)

        assert(data0 == data2)
        log.debug('test_lsb has finished!')
