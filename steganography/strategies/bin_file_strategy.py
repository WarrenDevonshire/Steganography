import numpy as np
from steganography.utilities.bits import set_bit
from steganography.utilities.rand import get_random_sequence


# TODO: Remove. Deprecated, replaced by lsb.py
def bin_file_merge(image, f_bin, seed):
    # convert image into a flat numpy array
    i_arr = np.array(image)
    i_shape = i_arr.shape
    i_arr = i_arr.ravel()

    # get size of both arrays
    upper_bound = len(i_arr)
    f_bin_size = len(f_bin)
    bits_in_f = f_bin_size * 8

    assert(bits_in_f + 32 < upper_bound)  # 32 for size info

    seq = get_random_sequence(0, upper_bound, seed)  # return a shuffled array of indexes for i_arr

    counter = 0  # used for index of seq

    # store f_bin_size in image as 4 bytes
    for byte in f_bin_size.to_bytes(length=4, byteorder='big', signed=False):
        byte_str = '{0:08b}'.format(byte)
        for bit in byte_str:
            i_arr[seq[counter]] = set_bit(i_arr[seq[counter]], 0, bit)
            counter = counter + 1

    # store f_bin in image
    for byte in f_bin:
        byte_str = '{0:08b}'.format(byte)
        for bit in byte_str:
            i_arr[seq[counter]] = set_bit(i_arr[seq[counter]], 0, bit)
            counter = counter + 1

    i_arr = i_arr.reshape(i_shape)
    # TODO: decide on whether or not to return an array or an image
    return i_arr


def bin_file_retrieve(image, seed):
    i_arr = np.array(image).ravel()  # get flat array from image

    upper_bound = len(i_arr)
    seq = get_random_sequence(0, upper_bound, seed)

    # TODO refactor size retrieval into testable function
    # retrieve first 32 bytes that contain the size information
    size_bit_str = ''
    for i in seq[:32]:
        bit = i_arr[i] % 2  # extract LSB from each byte
        size_bit_str += '{0:01b}'.format(bit & 1)

    file_size = int(size_bit_str, 2)
    assert(file_size * 8 < upper_bound)  # check the the number of bits in file does not exceed bytes in image

    file_bit_str = ''
    for i in seq[32: file_size * 8]:
        bit = i_arr[i] % 2
        file_bit_str += '{0:01b}'.format(bit & 1)

    file = int(file_bit_str, 2).to_bytes(length=file_size-4, byteorder='big', signed=False)
    return file
