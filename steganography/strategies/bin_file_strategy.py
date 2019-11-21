import numpy as np
from steganography.utilities.bits import set_bit
from steganography.utilities.rand import get_random_sequence


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
            counter += 1

    # store f_bin in image
    for byte in f_bin:
        byte_str = '{0:08b}'.format(byte)
        for bit in byte_str:
            i_arr[seq[counter]] = set_bit(i_arr[seq[counter]], 0, bit)
            counter = counter + 1

    i_arr = i_arr.reshape(i_shape)
    # TODO: decide on whether or not to return an array or an image
    return i_arr
