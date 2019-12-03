import numpy as np
from steganography.utilities.rand import get_random_sequence
from steganography.utilities.bits import set_bit
import logging
import math

SIZE_LENGTH = 32

# 24 bit pixel like:
# 3 MSB --> Blue LSB
# 2 MSB --> Green LSB
# 1 MSB --> Red LSB

PIXEL_ORDER = [(2, 2), (2, 1), (2, 0), (1, 1), (1, 0), (0, 0)]
SIZE_LENGTH = 32


def hide_data_in_blue(carry, data, seed):
    """

    :param carry:
    :param data:
    :param seed:
    :return:
    """
    upper_bound = (len(carry))
    data_size = len(data)

    logging.info("HIDE_DATA: Data size: %s", data_size / 8)
    logging.info("HIDE_DATA: Data size multiple of 6: %s", data_size / 6)
    carry_data_limit = (upper_bound * 6) // 8

    logging.info("HIDE_DATA: Carry limit is: %s bytes", carry_data_limit)
    logging.info("HIDE_DATA: Carry limit is: %s kilobytes", carry_data_limit / 1_000)
    logging.info("HIDE_DATA: Carry limit is: %s megabytes", carry_data_limit / 1_000_000)

    assert(data_size < (upper_bound * 6))
    seq = get_random_sequence(0, upper_bound, seed)
    compress_ratio = (float(data_size // 8) / float(carry_data_limit))

    logging.info("Data takes up: %s", compress_ratio * 100.0)

    # hide len information
    data_size = data_size // 8  # get data size in bytes
    size_bytes = data_size.to_bytes(length=SIZE_LENGTH // 8, byteorder='big', signed=False)
    size_bytes = np.frombuffer(size_bytes, dtype='uint8')
    size_bytes = np.unpackbits(size_bytes)
    logging.info("HIDE_DATA: size_bytes bit size: %s", len(size_bytes))
    assert (len(size_bytes) == SIZE_LENGTH)

    pixels_upper_bound = math.ceil(len(data) / 6)
    count = 0
    for index, bit in enumerate(size_bytes):
        random_index = seq[index]
        pixel_color, bit_index = PIXEL_ORDER[count]
        byte = carry[random_index][pixel_color]
        byte = set_bit(byte, bit_index, bit)
        carry[random_index][pixel_color] = byte
        count = count + 1
        count = count % 6


