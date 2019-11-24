from PIL import Image
import numpy as np
from numpy import random
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import binascii

CARRY_IMAGE_FILE = "c:/Users/cjmal/OneDrive/Desktop/Steganography/Steganography/steganography/resources/canyon1.png"
MESG_IMAGE_FILE = "c:/Users/cjmal/OneDrive/Desktop/Steganography/Steganography/steganography/resources/hello.png" 

def set_bit(byte, index, bit):
    # TODO: Write function documentation
    bit = int(bit, 2)
    bit_mask = 1 << index
    byte = byte & ~bit_mask
    if bit:
        byte = byte | bit_mask
    return byte

def binary_to_integer(binary):
    """
    Convert R or G or B pixel values from binary to integer.
    INPUT: A string tuple (e.g. ("00101010"))
    OUTPUT: Return an int tuple (e.g. (220))
    """
    return int(binary, 2)


def integer_to_binary(value):
    """
    Convert R or G or B pixel values from integer to binary
    INPUT: An integer tuple (e.g. (220))
    OUTPUT: A string tuple (e.g. ("00101010"))
    """
    return '{0:08b}'.format(value)

def get_seed(pass_code, salt):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits
        salt=salt,  # salt is 0x0000
        iterations=100000,
        backend=backend
    )
    return int(binascii.hexlify(kdf.derive(pass_code.encode())), 16)

def get_random_sequence(lower_bound, upper_bound, seed):
    # TODO: Write function documentation
    sequence = np.arange(lower_bound, upper_bound)
    random.seed(seed)
    random.shuffle(sequence)
    return sequence

#utilize two lsb of carry_byte and insert one msb of secret_byte
def construct_r_byte(carry_byte, message_byte):
    carr_byte = str(integer_to_binary(carry_byte))
    mesg_byte = str(integer_to_binary(message_byte))
    new_carr_byte = carr_byte
    #new_carr_byte = carr_byte[0:7] + mesg_byte[0] 
    new_carr_byte = int(new_carr_byte, 2)
    return new_carr_byte

#utilize two lsb of carry_byte and insert two msb of secret_byte
def construct_g_byte(carry_byte, message_byte):
    
    carr_byte = str(integer_to_binary(carry_byte))
    mesg_byte = str(integer_to_binary(message_byte))
    #new_carr_byte = carr_byte[0:6] + mesg_byte[0:2] 
    new_carr_byte = carr_byte
    new_carr_byte = int(new_carr_byte, 2)
    return new_carr_byte

#utilize three lsb of carry_byte and insert three msb of secret_byte
def construct_b_byte(carry_byte, message_byte):
    
    carr_byte = str(integer_to_binary(carry_byte))
    mesg_byte = str(integer_to_binary(message_byte))
    #new_carr_byte = carr_byte[0:5] + mesg_byte[0:3] 
    new_carr_byte = carr_byte
    new_carr_byte = int(new_carr_byte, 2)
    return new_carr_byte

def deconstruct_r_byte(carry_byte):
    carr_byte = str(integer_to_binary(carry_byte))
    #new_carr_byte = carr_byte[7] + "0000000"
    new_carr_byte = carr_byte
    new_carr_byte = int(new_carr_byte, 2)
    return new_carr_byte

def deconstruct_g_byte(carry_byte):
    carr_byte = str(integer_to_binary(carry_byte))
    #new_carr_byte = carr_byte[6:] + "000000"
    new_carr_byte = carr_byte
    new_carr_byte = int(new_carr_byte, 2)
    return new_carr_byte

def deconstruct_b_byte(carry_byte):
    carr_byte = str(integer_to_binary(carry_byte))
    #new_carr_byte = carr_byte[5:] + "00000"
    new_carr_byte = carr_byte
    new_carr_byte = int(new_carr_byte, 2)
    return new_carr_byte

def construct_new_carry(carry, message):
    carr_img = Image.open(carry)
    mesg_img = Image.open(message)

    carr_width = carr_img.size[0]  # x
    carr_length = carr_img.size[1]  # y

    mesg_size = mesg_img.size

    carr_arr = np.array(carr_img)
    mesg_arr = np.array(mesg_img)

    carr_r, carr_g, carr_b = carr_arr[:,:,0].ravel(), carr_arr[:,:,1].ravel(), carr_arr[:,:,2].ravel()
    mesg_r, mesg_g, mesg_b = mesg_arr[:,:,0].ravel(), mesg_arr[:,:,1].ravel(), mesg_arr[:,:,2].ravel()

    sequence = get_random_sequence(0, len(mesg_r), 10)
    print(sequence[0:10])

    # seed = get_seed(pass_code="Hello there man", salt=bytes(4))
    # seed = seed % (2 ** 32 - 1)
    # print(seed)
    # sequence = get_random_sequence(0, len(mesg_r), seed)
    # print(sequence)

    count=0

    for i in range(0,len(mesg_r)):
        mesg_r_byte = mesg_r[i]
        mesg_g_byte = mesg_g[i]
        mesg_b_byte = mesg_b[i]

        carr_r_byte = carr_r[sequence[i]]
        carr_g_byte = carr_g[sequence[i]]
        carr_b_byte = carr_b[sequence[i]]

        new_carr_r_byte = construct_r_byte(carr_r_byte, mesg_r_byte)
        new_carr_g_byte = construct_g_byte(carr_g_byte, mesg_g_byte)
        new_carr_b_byte = construct_b_byte(carr_b_byte, mesg_b_byte)

        carr_r[sequence[i]] = new_carr_r_byte
        carr_g[sequence[i]] = new_carr_g_byte
        carr_b[sequence[i]] = new_carr_b_byte

        count = count + 1

    carr_r = np.matrix(carr_r)
    carr_r = np.asarray(carr_r).reshape(carr_length, carr_width)

    carr_g = np.matrix(carr_g)
    carr_g = np.asarray(carr_g).reshape(carr_length, carr_width)

    carr_b = np.matrix(carr_b)
    carr_b = np.asarray(carr_b).reshape(carr_length, carr_width)

    carr_arr[:,:,0] = carr_r
    carr_arr[:,:,1] = carr_g
    carr_arr[:,:,2] = carr_b
    
    img = Image.fromarray(carr_arr, 'RGB')
    return img, mesg_size, len(mesg_arr)

def pull_out_secret(carry, message):
    carr_img = Image.open(carry)
    mesg_img = Image.open(message)

    width = mesg_img.size[0]
    length = mesg_img.size[1]

    #new_img = Image.new('RGB', (width, length))
    new_img = mesg_img
    new_img.show()

    carr_arr = np.array(carr_img)
    mesg_arr = np.array(mesg_img)
    new_arr = np.array(new_img)

    carr_r, carr_g, carr_b = carr_arr[:,:,0].ravel(), carr_arr[:,:,1].ravel(), carr_arr[:,:,2].ravel()
    mesg_r, mesg_g, mesg_b = mesg_arr[:,:,0].ravel(), mesg_arr[:,:,1].ravel(), mesg_arr[:,:,2].ravel()
    new_r, new_g, new_b = new_arr[:,:,0].ravel(), new_arr[:,:,1].ravel(), new_arr[:,:,2].ravel()

    print("Before")
    print(mesg_r)
    print(mesg_g)
    print(mesg_b)
    print()
    print(new_r)
    print(new_g)
    print(new_b)

    sequence = get_random_sequence(0, len(new_r), 10)
    print(sequence[0:10])
    # seed = get_seed(pass_code="Hello there man", salt=bytes(4))
    # seed = seed % (2 ** 32 - 1)
    # # print(seed)
    # sequence = get_random_sequence(0, len(new_r), seed)
    # print(sequence)

    count = 0

    for i in range(0,len(new_r)):
        carr_r_byte = carr_r[sequence[i]]
        #print(carr_r_byte)
        carr_g_byte = carr_g[sequence[i]]
        carr_b_byte = carr_b[sequence[i]]

        # mesg_r_byte = deconstruct_r_byte(carr_r_byte)
        # mesg_g_byte = deconstruct_g_byte(carr_g_byte)
        # mesg_b_byte = deconstruct_b_byte(carr_b_byte)
        
        # new_r[i] = mesg_r_byte
        # new_g[i] = mesg_g_byte
        # new_b[i] = mesg_b_byte

        new_r[i] = carr_r_byte
        #print(new_r[i])
        new_g[i] = carr_g_byte
        new_b[i] = carr_b_byte

        count = count + 1

    print("After")
    print(mesg_r)
    print(mesg_g)
    print(mesg_b)
    print()
    print(new_r)
    print(new_g)
    print(new_b)
    print()

    new_mesg_r = np.matrix(new_r)
    new_mesg_r = np.asarray(new_r).reshape(length, width)

    new_mesg_g = np.matrix(new_g)
    new_mesg_g = np.asarray(new_g).reshape(length, width)

    new_mesg_b = np.matrix(new_b)
    new_mesg_b = np.asarray(new_b).reshape(length, width)

    new_arr[:,:,0] = new_mesg_r
    new_arr[:,:,1] = new_mesg_g
    new_arr[:,:,2] = new_mesg_b

    img = Image.fromarray(new_arr, 'RGB')
    return img


def main():
    img = construct_new_carry(CARRY_IMAGE_FILE, MESG_IMAGE_FILE)
    img[0].show()

    test = pull_out_secret(CARRY_IMAGE_FILE, MESG_IMAGE_FILE)
    test.show()

    # print(deconstruct_g_byte(187))


if __name__ == "__main__":
    main()