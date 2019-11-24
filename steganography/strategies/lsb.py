import numpy as np
from steganography.utilities.rand import get_random_sequence


def hide_data_in_LSB(carry, data, seed=0):
    """Hide data in carry and return a numpy array.

    Keyword arguments:
    carry -- the one dimensional array to hide data in
    data -- an array of bits to hide
    seed -- an integer (default = 0)
    """
    upper_bound = (len(carry) // 8) * 8
    data_size = len(data)

    assert(data_size < upper_bound)

    seq = get_random_sequence(0, upper_bound, seed)

    for index, bit in enumerate(data):
        random_index = seq[index]
        bit_mask = 1
        byte = carry[random_index] & ~bit_mask
        if bit:
            byte = byte | bit_mask
        carry[random_index] = byte

    return carry


def get_data_in_LSB(carry, seed=0):
    upper_bound = (len(carry) // 8) * 8

    seq = get_random_sequence(0, upper_bound, seed)

    bits = np.empty(upper_bound, dtype='uint8')

    for index, random_index in enumerate(seq):
        bits[index] = carry[random_index] % 2

    return np.packbits(bits)
