import binascii
from io import BytesIO

import numpy as np
from numpy import random
from PIL import Image

CARRY_IMAGE_PATH = "../Images/hello.png"
SECRET_IMAGE_PATH = "../Images/basi0g01.png"
PNG_HEADER_SIG = binascii.hexlify(b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a")


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
    s_file_size = len(s_bin)
    bits_in_s = s_file_size * 8  # number of bits in s_bin
    # print(bits_in_s, c_upper_bound, c_shape)
    assert (bits_in_s + 32 < c_upper_bound)  # number of bits in s must be less than bytes in c + 32 for size info

    seq = get_random_sequence(0, c_upper_bound, seed) # return a shuffled array of indexes for c_arr
    counter = 0  # used for index of sequence.
    # store secret_file_size in carry image.
    s_file_size_bytes = s_file_size.to_bytes(length=4, byteorder='big', signed=False)
    for byte in s_file_size_bytes:
        byte_str = '{0:08b}'.format(byte)
        for bit in byte_str:
            c_arr[seq[counter]] = set_bit(c_arr[seq[counter]], 0, bit)
            counter = counter + 1

    # store secret_file in carry image.
    for byte in s_bin:
        byte_str = '{0:08b}'.format(byte)
        for bit in byte_str:
            c_arr[seq[counter]] = set_bit(c_arr[seq[counter]], 0, bit)
            counter = counter + 1

    c_arr = c_arr.reshape(c_shape)
    c_image = Image.fromarray(c_arr, c_image.mode)
    return c_image


def random_retrieve(carry_image, seed):
    c_arr = np.array(carry_image).ravel()
    c_upper_bound = len(c_arr)
    seq = get_random_sequence(0, c_upper_bound, seed)

    c_file = []

    for i in range(0, 64+32):
        random_index = seq[i]
        c_file.append(c_arr[random_index])

    c_bit_str = ''
    for byte in c_file:
        bit = byte % 2
        c_bit_str += '{0:01b}'.format(bit & 1)

    s_file_size = int(c_bit_str[:32], 2)  # .to_bytes(length=4, byteorder='big', signed=False)
    assert(s_file_size * 8 < c_upper_bound)  # check that number of bits in s_file is less than bytes in c_arr
    print("Secret file is", s_file_size, "bytes long")  # print the length of file in bytes
    h = int(c_bit_str[32:], 2).to_bytes(length=8, byteorder='big', signed=False)
    assert(binascii.hexlify(h) == PNG_HEADER_SIG)
    print("PNG Header Sig: ", binascii.hexlify(h))  # print the png header signature

    for i in range(64+32, s_file_size * 8):
        random_index = seq[i]
        bit = c_arr[random_index] % 2
        c_bit_str += '{0:01b}'.format(bit & 1)
    s_file = int(c_bit_str[32:], 2).to_bytes(length=s_file_size-4, byteorder='big', signed=False)
    print(s_file)

    return Image.open(BytesIO(s_file))


image = random_merge(CARRY_IMAGE_PATH, SECRET_IMAGE_PATH, 0)
random_retrieve(image, 0).show()
