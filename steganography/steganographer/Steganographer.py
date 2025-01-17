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
        self._compression = compression
        self._encryption = encryption
        self._log = logging.getLogger(__name__)
        self._log.debug('Steganographer created!')

    def hide_data_from_file(self, path, out_path, strategy, passcode):
        self._log.debug('hide_data_from_file() has begun!')
        with open(path, 'rb') as f:
            data = f.read()

        # compress and encrypt data
        if self._compression:
            data = compress_data(data)

        key, seed = generate_key_and_seed(passcode)
        if self._encryption:
            data = encrypt(data, key)

        # transform data into bit array
        data = np.frombuffer(data, dtype='uint8')
        data = np.unpackbits(data)

        # apply strategy
        image = np.reshape(strategy(np.copy(self._pixels), data, seed), self._pixels.shape)
        image = Image.fromarray(image)
        image.save(out_path)
        self._log.debug('hide_data_from_file() has finished!')

    def get_data_from_image(self, out_path, strategy, passcode):
        self._log.debug('get_data_from_image() has begun!')

        # apply strategy
        key, seed = generate_key_and_seed(passcode)
        data = strategy(self._pixels, seed).tobytes()

        # compress and encrypt data
        if self._encryption:
            data = decrypt(data, key)

        if self._compression:
            data = decompress_data(data)

        # save data to out_path
        with open(out_path, 'wb') as f:
            f.write(data)
        self._log.debug('get_data_from_image() has finished!')
