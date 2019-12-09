from PIL import Image
import numpy as np
import logging

from steganography.utilities.aes import encrypt, decrypt, generate_key_and_seed
from steganography.utilities.compression import compress_data, decompress_data


class Steganographer:

    def __init__(self, image_file_path, encryption, compression):
        with Image.open(image_file_path) as image:
            self._pixels = np.array(image)
        self._pixels.setflags(write=False)
        self.compression = compression
        self.encryption = encryption
        self.log = logging.getLogger(__name__)
        self.log.debug('Steganographer created!')

    def hide_data_from_file(self, path, out_path, strategy, passcode):
        self.log.debug('hide_data_from_file() has begun!')
        with open(path, 'rb') as f:
            data = f.read()

        # compress and encrypt data
        if self.compression:
            data = compress_data(data)

        key, seed = generate_key_and_seed(passcode)
        if self.encryption:
            data = encrypt(data, key)

        # transform data into bit array
        data = np.frombuffer(data, dtype='uint8')
        data = np.unpackbits(data)

        # apply strategy
        image = np.reshape(strategy(np.copy(self._pixels), data, seed), self._pixels.shape)
        image = Image.fromarray(image)
        image.save(out_path)
        self.log.debug('hide_data_from_file() has finished!')

    def get_data_from_image(self, image_path, out_path, strategy, passcode):
        self.log.debug('get_data_from_image() has begun!')
        with Image.open(image_path) as image:
            pixels = np.array(image)

        # apply strategy
        key, seed = generate_key_and_seed(passcode)
        data = strategy(pixels, seed)

        # compress and encrypt data
        if self.encryption:
            data = decompress_data(data, key)

        if self.compression:
            data = decompress_data(data)

        # save data to out_path
        with open(out_path, 'wb') as f:
            f.write(data)
        self.log.debug('get_data_from_image() has finished!')
