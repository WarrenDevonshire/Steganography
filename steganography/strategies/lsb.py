import numpy as np
from steganography.utilities.rand import get_random_sequence
import logging


def hide_data_in_LSB(carry, data, seed=0):
    """Hide data in carry and return a numpy array.

    Keyword arguments:
    carry -- the one dimensional array to hide data in
    data -- an array of bits to hide
    seed -- an integer (default = 0)
    """
    carry = carry.ravel()
    upper_bound = (len(carry) // 8) * 8
    data_size = len(data)

    logging.info("upper_bound: %s", upper_bound)
    logging.info("data_size: %s", data_size)

    assert(data_size < upper_bound)

    seq = get_random_sequence(0, upper_bound, seed)
    logging.info("seq: %s", len(seq))

    size_bytes = data_size.to_bytes(length=4, byteorder='big', signed=False)
    size_bytes = np.frombuffer(size_bytes, dtype='uint8')
    size_bytes = np.unpackbits(size_bytes)
    assert(len(size_bytes) == 32)

    for index, bit in enumerate(size_bytes):
        random_index = seq[index]
        bit_mask = 1
        byte = carry[random_index] & ~bit_mask
        if bit:
            byte = byte | bit_mask
        carry[random_index] = byte

    offset = len(size_bytes)

    for index, bit in enumerate(data):
        random_index = seq[index + offset]
        bit_mask = 1
        byte = carry[random_index] & ~bit_mask
        if bit:
            byte = byte | bit_mask
        carry[random_index] = byte

    logging.info("carry: %s", len(carry))
    return carry


def get_data_in_LSB(carry, seed=0):
    upper_bound = (len(carry) // 8) * 8
    logging.info("upper_bound: %s", upper_bound)
    seq = get_random_sequence(0, upper_bound, seed)
    logging.info("seq: %s", len(seq))

    size_bits = np.empty(32, dtype='uint8')
    offset = len(size_bits)

    for index, random_index in enumerate(seq[:offset]):
        size_bits[index] = carry[random_index] % 2

    bits = np.empty(upper_bound, dtype='uint8')
    logging.info("bits: %s", len(bits))

    offset = np.packbits(size_bits)
    upper_bound = int.from_bytes(offset, byteorder='big', signed=False)
    logging.info("seq offset: %s", len(seq[offset_bits:offset]))
    logging.info("offset: %s", offset)
    for index, random_index in enumerate(seq[offset:]):
        bits[index] = carry[random_index] % 2
    logging.info("bits to bytes: %s", len(bits) // 8)
    data = np.packbits(bits)
    logging.info("data packed: %s", len(data))
    return data
