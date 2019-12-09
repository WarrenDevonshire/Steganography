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
    log = logging.getLogger(__name__)
    log.debug('hide_data_in_LSB() has been called!')
    carry = carry.ravel()
    upper_bound = (len(carry) // 8) * 8
    data_size = len(data)
    # TODO: create data_limit variable

    log.debug(f'upper_bound length: {upper_bound}')
    log.debug(f'data length: {data_size}')
    log.info(f'Data limit in image is: {(len(carry) // 8) / 1_000} kilobytes')

    assert(data_size < upper_bound - 32)

    seq = get_random_sequence(0, upper_bound, seed)
    log.debug(f'seq length: {len(seq)}')

    data_size = data_size // 8
    log.debug(f'data_size: {data_size} bytes')
    size_bytes = data_size.to_bytes(length=SIZE_LENGTH // 8, byteorder='big', signed=False)
    log.debug(f'size_bytes: {size_bytes}')
    size_bytes = np.frombuffer(size_bytes, dtype='uint8')
    size_bytes = np.unpackbits(size_bytes)
    assert(len(size_bytes) == SIZE_LENGTH)  # sanity check

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

    log.debug('hide_data_in_LSB() has finished!')
    return carry


def get_data_in_LSB(carry, seed):
    """
    Get data from carry and return a numpy array of bytes.
    :param carry: an np array image
    :param seed: an integer
    :return: an np array of bytes
    """
    log = logging.getLogger(__name__)
    log.debug('get_data_in_LSB() has been called!')
    seq = get_random_sequence(0, ((len(carry) // 8) * 8), seed)
    log.debug(f'seq length: {len(seq)}')

    size_bits = np.empty(SIZE_LENGTH, dtype='uint8')

    for index, random_index in enumerate(seq[:len(size_bits)]):
        size_bits[index] = carry[random_index] % 2

    data_size = int.from_bytes(np.packbits(size_bits), byteorder='big', signed=False) * 8  # size in bits
    log.debug(f'data_size: {data_size} bytes')
    assert(data_size <= len(seq) - 32)
    data_bits = np.empty(data_size, dtype='uint8')

    for index, random_index in enumerate(seq[SIZE_LENGTH:(data_size + SIZE_LENGTH)]):
        data_bits[index] = carry[random_index] % 2
    data_bytes = np.packbits(data_bits)
    log.debug(f'data_bytes len: {len(data_bytes)}')
    log.debug(f'get_data_in_LSB() has finished!')
    return data_bytes
