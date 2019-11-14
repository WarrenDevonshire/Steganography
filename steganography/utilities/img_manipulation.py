from PIL import Image
import numpy as np


def to_array(image):
    image_arr = np.array(image)
    shape = image_arr.shape
    flat_arr = image_arr.ravel()

    return flat_arr, shape


def to_image(arr, img_shape):
    matrix = np.matrix(arr)

    reform_matrix = np.asarray(matrix).reshape(img_shape)

    new_img = Image.fromarray(reform_matrix, 'RGB')

    return new_img


def merge_pixels(pixel1, pixel2):
    """
    Merge two R or G or B pixels using 4 least significant bits.
    INPUT: A string tuple (e.g. ("00101010")),
           Another string tuple (e.g. ("00101010"))
    OUTPUT: An integer tuple with the two RGB values merged 00100010
    """

    merged_pixel = (pixel1[:4] + pixel2[:4])
    return merged_pixel
