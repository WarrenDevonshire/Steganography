import numpy as np
from PIL import Image


def pil_to_array(path_to_image):
    with Image.open(path_to_image) as pil_image:
        image = np.array(pil_image)
    return image.ravel(), image.shape


def random_merge(path_to_carry, path_to_secret, seed):
    with Image.open(path_to_carry) as c_image, open(path_to_secret, 'rb') as s_file:
        c_arr = np.array(c_image)
        c_shape = c_image.shape
        s_bin = s_file.read()
