import argparse
from PIL import Image
from steganography.utilities.hash import get_seed
from steganography.strategies.lsb import get_data_in_LSB, hide_data_in_LSB
from steganography.core.Steganographer import Steganographer


# TODO: Add flags for strategy selection
# TODO: Remove unnecessary png files from resources.
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("carry", help="path to carry image")
    parser.add_argument("secret", help="path to secret file to hide")
    parser.add_argument("-d", "--decrypt", help="retrieve hidden data from image", action='store_true')
    parser.add_argument("-o", "--output", help="path to store program output")
    args = parser.parse_args()
    st = Steganography()
    if not args.decrypt:
        st.set_output_path(args.output)
        st.hide_data(args.carry, args.secret, hide_data_in_LSB)
    else:
        st.set_output_path(args.secret)
        st.get_data(args.carry, get_data_in_LSB)


class Steganography:

    def __init__(self):
        self.path_to_output = "./output.png"

    def set_output_path(self, path_to_output):
        self.path_to_output = path_to_output

    def hide_data(self, path_to_carry, path_to_secret, strategy):
        st = Steganographer(path_to_carry)
        passcode = ''  # TODO: get passcode from stdin
        st.hide_data_from_file(path=path_to_secret, out_path=self.path_to_output, strategy=strategy, passcode=passcode)

    def get_data(self, path_to_carry, strategy):
        passcode = ''  # TODO: get passcode from stdin
        Steganographer.get_data_from_image(image_path=path_to_carry, out_path=self.path_to_output, strategy=get_data_in_LSB, passcode=passcode)
