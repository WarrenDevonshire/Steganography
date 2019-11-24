from steganography.strategies.lsb import hide_data_in_LSB, get_data_in_LSB
from steganography.utilities.rand import get_random_sequence
from steganography.utilities.compression import compress_data, decompress_data
import numpy as np


def hide_compressed_data(carry, data, seed=0):
    data = compress_data(data)
    data = np.frombuffer(data, dtype='uint8')
    data = np.unpackbits(data)
    return hide_data_in_LSB(carry, data, seed)


def get_compressed_data(carry, seed=0):
    data = get_data_in_LSB(carry, seed)
    return decompress_data(data)
