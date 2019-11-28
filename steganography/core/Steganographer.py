from PIL import Image
import numpy as np
import logging

from steganography.utilities.aes import encrypt, decrypt, generate_key_and_seed
from steganography.utilities.compression import compress_data, decompress_data


def _pack_data(data, key):
    # compress and encrypt data
    data = compress_data(data)
    logging.info("compressed data size: %s", len(data))
    data = encrypt(data, key)
    logging.info("encrypted data size: %s", len(data))
    # transform data into bit array
    data = np.frombuffer(data, dtype='uint8')
    print("Pack Buffer:", data)
    return np.unpackbits(data)


def _unpack_data(data, key):
    # decrypt and decompress data
    data = data.tobytes()
    data = decrypt(data, key)
    logging.info("decrypted data size: %s", len(data))
    data = decompress_data(data)
    logging.info("decompressed data size: %s", len(data))
    return data


class Steganographer:

    def __init__(self, image_file_path):
        with Image.open(image_file_path) as image:
            self._pixels = np.array(image)
        self._pixels.setflags(write=False)  # Should this be immutable?

    def hide_data_from_file(self, path, out_path, strategy, passcode=''):
        with open(path, 'rb') as f:
            data = f.read()

        # compress, encrypt, and transform data into a bit array
        key, seed = generate_key_and_seed(passcode)
        data = _pack_data(data, key)

        # apply strategy
        image = np.reshape(strategy(np.copy(self._pixels), data, seed), self._pixels.shape)
        image = Image.fromarray(image)
        image.save(fp=out_path)

    @staticmethod
    def get_data_from_image(image_path, out_path, strategy, passcode=''):
        with Image.open(image_path) as image:
            pixels = np.array(image)
        # flatten pixels
        pixels = pixels.ravel()

        key, seed = generate_key_and_seed(passcode)

        # apply strategy
        data = strategy(pixels, seed)

        # decompress, decrypt, and transform data into byte array
        data = _unpack_data(data, key)

        # save data to out_path
        with open(out_path, 'wb') as f:
            f.write(data)
