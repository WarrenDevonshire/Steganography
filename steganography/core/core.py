import argparse
from PIL import Image
from steganography.utilities.hash import get_seed
from steganography.strategies.bin_strategy import random_retrieve, random_merge


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("carry", help="path to carry image")
    parser.add_argument("secret", help="path to secret file to hide")
    parser.add_argument("-o", "--output", help="path to store program output")
    args = parser.parse_args()
    steg = Steganography(get_seed(pass_code="hello hello hello", salt=bytes(4)))
    steg.set_output_path(args.output)
    steg.hide_data(args.carry, args.secret, random_merge)


class Steganography:

    def __init__(self, seed):
        self.path_to_output = "./output.png"
        self.seed = seed

    def set_output_path(self, path_to_output):
        self.path_to_output = path_to_output

    def hide_data(self, path_to_carry, path_to_secret, strategy):
        image = strategy(path_to_carry, path_to_secret, self.seed)
        image.save(self.path_to_output)

    def get_data(self, path_to_carry, strategy):
        with Image.open(path_to_carry) as c_image:
            out_image = strategy(c_image, self.seed)
            out_image.save(self.path_to_output)
