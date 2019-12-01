import numpy as np
from steganography.utilities.rand import get_random_sequence
import logging

SIZE_LENGTH = 32


def hide_data_in_LSB(carry, data, seed):
    """
    Hide data in carry and return a numpy array.
    :param carry: an np array image to hide data in
    :param data: an array of bits to hide
    :param seed: an integer
    :return: flattened carry is returned
    """
    carry = carry.ravel()
    upper_bound = (len(carry) // 8) * 8
    data_size = len(data)

    logging.info("HIDE_DATA: Data size: %s", data_size // 8)
    logging.info("HIDE_DATA: Carry limit is: %s bytes", len(carry) // 8)
    logging.info("HIDE_DATA: Carry limit is: %s kilobytes", (len(carry) // 8) / 1_000)
    logging.info("HIDE_DATA: Carry limit is: %s megabytes", (len(carry) // 8) / 1_000_000)

    assert(data_size < upper_bound)

    seq = get_random_sequence(0, upper_bound, seed)
    logging.info("HIDE_DATA: Random sequence length: %s", len(seq))

    data_size = data_size // 8
    size_bytes = data_size.to_bytes(length=SIZE_LENGTH // 8, byteorder='big', signed=False)
    size_bytes = np.frombuffer(size_bytes, dtype='uint8')
    size_bytes = np.unpackbits(size_bytes)
    logging.info("HIDE_DATA: size_bytes bit size: %s", len(size_bytes))
    assert(len(size_bytes) == SIZE_LENGTH)

    # TODO: Code duplication
    for index, bit in enumerate(size_bytes):
        random_index = seq[index]
        bit_mask = 1
        byte = carry[random_index] & ~bit_mask
        if bit:
            byte = byte | bit_mask
        carry[random_index] = byte

    for index, bit in enumerate(data):
        random_index = seq[index + SIZE_LENGTH]
        bit_mask = 1
        byte = carry[random_index] & ~bit_mask
        if bit:
            byte = byte | bit_mask
        carry[random_index] = byte

    return carry


# TODO: In Progress. Status: Broken
def get_data_in_LSB(carry, seed):
    """
    Get data from carry and return a numpy array of bytes.
    :param carry: an np array image
    :param seed: an integer
    :return: an np array of bytes
    """
    seq = get_random_sequence(0, ((len(carry) // 8) * 8), seed)
    logging.info("GET_DATA: Random sequence length: %s", len(seq))

    size_bits = np.empty(SIZE_LENGTH, dtype='uint8')

    for index, random_index in enumerate(seq[:len(size_bits)]):
        size_bits[index] = carry[random_index] % 2

    data_size = int.from_bytes(np.packbits(size_bits), byteorder='big', signed=False) * 8  # size in bits
    logging.info("GET_DATA: data_size retrieved from carry: %s", data_size // 8)
    assert(data_size <= len(seq))
    data_bits = np.empty(data_size, dtype='uint8')
    logging.info("GET_DATA: Data size: %s", len(data_bits) // 8)

    for index, random_index in enumerate(seq[SIZE_LENGTH:(data_size + SIZE_LENGTH)]):
        data_bits[index] = carry[random_index] % 2
    data_bytes = np.packbits(data_bits)
    return data_bytes
