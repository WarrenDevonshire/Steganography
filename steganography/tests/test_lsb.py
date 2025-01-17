import unittest
from PIL import Image
import numpy as np
import logging
from steganography.tests.COMMON import IMAGES, DATA

from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB
from steganography.utilities.aes import generate_key_and_seed, encrypt, decrypt

PASSCODE = "Hello, World!"


class TestLsb(unittest.TestCase):

    def test_lsb(self):
        # create logger
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.FileHandler('test_lsb_logs/test_lsb.log')
        ch.setLevel(level=logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        log.addHandler(ch)

        log.debug('test_lsb() has started!')
        with Image.open(IMAGES['1mb']) as image, open(DATA['150kb'], 'rb') as file:
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
        log.debug('test_lsb() has finished!')
