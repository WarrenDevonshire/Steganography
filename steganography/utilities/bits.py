def set_bit(byte, index, bit):
    # TODO: Write function documentation
    bit_mask = 1 << index
    byte = byte & ~bit_mask
    if bit:
        byte = byte | bit_mask
    return byte


def read_lsb(byte):
    # TODO: Write function documentation
    return '{0:01b}'.format(byte & 1)


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