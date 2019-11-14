from steganography.strategies.bin_strategy import random_merge, random_retrieve
from steganography.strategies.merge_strategy import merge_images, extract_hidden_image
from steganography.utilities.hash import get_seed
# TODO remove after testing.
CARRY_IMAGE_PATH = "./resources/hello.png"
SECRET_IMAGE_PATH = "./resources/basi0g01.png"
CARRY_IMAGE_FILE = "./resources/canyon1.png"
MESG_IMAGE_FILE = "./resources/hello.png"
MERGED_IMAGE_FILE = "./resources/merged.png"


def run():
    print("Start!")
    image = random_merge(CARRY_IMAGE_PATH, SECRET_IMAGE_PATH, 0)
    image.show()
    image = random_retrieve(image, 0)
    image.show()
    print("Finish!")

    secretKey = get_seed(pass_code="blah blah blah", salt=bytes(4))

    merged_image = merge_images(CARRY_IMAGE_FILE, MESG_IMAGE_FILE, secretKey)
    merged_image.show()

    hidden_image = extract_hidden_image(MERGED_IMAGE_FILE, MESG_IMAGE_FILE, secretKey)
    hidden_image.show()
