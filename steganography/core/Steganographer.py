from PIL import Image
import numpy as np

from steganography.utilities.aes import encrypt, decrypt, generate_key_and_seed
from steganography.utilities.compression import compress_data, decompress_data


class Steganographer:

    def __init__(self, image_file_path):
        with Image.open(image_file_path) as image:
            self._pixels = np.array(image)
        self._pixels.setflags(write=False)  # Should this be immutable?

    def hide_data_from_file(self, path, out_path, strategy, passcode=''):
        with open(path, 'rb') as f:
            data = f.read()

        # compress and encrypt data
        key, seed = generate_key_and_seed(passcode)
        data = self._prepare_data(data, key)

        # transform data into bit array
        data = np.array(data, dtype='uint8')
        data = np.unpackbits(data)

        # apply strategy
        image = Image.fromarray(strategy(np.copy(self._pixels), data, seed))
        image.save(fp=out_path)

    def _prepare_data(self, data, key):
        data = compress_data(data)
        return encrypt(data, key)
