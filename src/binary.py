import binascii

import numpy as np
from numpy import random
from PIL import Image

CARRY_IMAGE_PATH = "../Images/hello.png"
SECRET_IMAGE_PATH = "../Images/basi0g01.png"


def set_bit(byte, index, bit):
    bit = int(bit, 2)
    bit_mask = 1 << index
    byte = byte & ~bit_mask
    if bit:
        byte = byte | bit_mask
    return byte


def read_lsb(byte):
    return '{0:01b}'.format(byte & 1)


def get_random_sequence(lower_bound, upper_bound, seed):
    sequence = np.arange(lower_bound, upper_bound)
    random.seed(seed)
    random.shuffle(sequence)
    return sequence


def random_merge(path_to_carry, path_to_secret, seed):
    with Image.open(path_to_carry) as c_image, open(path_to_secret, 'rb') as s_file:
        c_arr = np.array(c_image)
        c_shape = c_arr.shape
        c_arr = c_arr.ravel()
        s_bin = s_file.read()

    c_upper_bound = len(c_arr)
    bits_in_s = len(s_bin) * 8
    # print(bits_in_s, c_upper_bound, c_shape)
    assert (bits_in_s < c_upper_bound)  # number of bits in s must be less than bytes in c

    seq = get_random_sequence(0, c_upper_bound, seed)
    counter = 0
    temp = []
    for i in range(0, 100):
        temp.append(c_arr[seq[i]])
    print(temp)
    for byte in s_bin:
        byte_str = '{0:08b}'.format(byte)
        for bit in byte_str:
            c_arr[seq[counter]] = set_bit(c_arr[seq[counter]], 0, bit)
            counter = counter + 1
    temp = []
    for i in range(0, 100):
        temp.append(c_arr[seq[i]])
    print(temp)
    c_arr = c_arr.reshape(c_shape)
    c_image = Image.fromarray(c_arr, c_image.mode)
    return c_image


def random_retrieve(carry_image, seed):
    c_arr = np.array(carry_image).ravel()
    c_upper_bound = len(c_arr)
    seq = get_random_sequence(0, c_upper_bound, seed)
    header = []
    for i in range(0, 64):
        random_index = seq[i]
        header.append(c_arr[random_index])
    header_bits = []
    byte_str = ''
    for byte in header:
        bit = byte % 2
        byte_str += '{0:01b}'.format(bit & 1)
        header_bits.append(byte % 2)
    print(header)
    print(byte_str, len(byte_str))
    h = int(byte_str, 2).to_bytes(length=8, byteorder='big', signed=False)
    print(binascii.hexlify(h))
    print(binascii.hexlify(b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"))


image = random_merge(CARRY_IMAGE_PATH, SECRET_IMAGE_PATH, 0)
random_retrieve(image, 0)
