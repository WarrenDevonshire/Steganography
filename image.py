# Author: Dr. Baliga
# Illustration of image manipulation using the Pillow python library

from PIL import Image
from functools import partial

IMAGE_FILE = "canyon.jpg"  # Enter the name of your image here.

im = Image.open(IMAGE_FILE)
print(im.format, im.size, im.mode)
im.show()


def flipbits(val, n):  # Flip n least significant bits in val
    return val ^ ((1 << n) - 1)


flipbits(17, 3)  # 17 = 10001 in binary, so if you flip 3 least significant bits, you get 10110 which equals 22


def modimage(im, func):  # Apply specified function func to each pixel.
    px = im.load()  # Get the pixels in the image

    # Loop through all pixels and modify their r, g, b values
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            p = px[i, j]  # get the r,g,b values for this pixel
            r = func(p[0])
            g = func(p[1])
            b = func(p[2])
            px[i, j] = (r, g, b)
    im.show()


#     im.save("tmp.jpg") # You can save the modified image


modimage(Image.open(IMAGE_FILE), partial(flipbits, n=6))
