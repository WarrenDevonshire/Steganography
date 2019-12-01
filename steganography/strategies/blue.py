import numpy as np
from steganography.utilities.rand import get_random_sequence
import logging

SIZE_LENGTH = 32

# 24 bit pixel like:
# 3 MSB --> Blue LSB
# 2 MSB --> Green LSB
# 1 MSB --> Red LSB


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
    carry_data_limit = (upper_bound * 6) / 8

    logging.info("HIDE_DATA: Carry limit is: %s bytes", carry_data_limit)
    logging.info("HIDE_DATA: Carry limit is: %s kilobytes", carry_data_limit / 1_000)
    logging.info("HIDE_DATA: Carry limit is: %s megabytes", carry_data_limit / 1_000_000)

    assert(data_size < (upper_bound * 6))

    compress_ratio = (float(carry_data_limit) - float(data_size // 8)) / float(carry_data_limit)

    logging.info("Data takes up: %d%%" % (100.0 * compress_ratio))
