import logging
import argparse
from steganography.strategies.lsb import get_data_in_LSB, hide_data_in_LSB
from steganography.steganographer.Steganographer import Steganographer

HIDE_STRATEGIES = {
    "lsb": hide_data_in_LSB
}
GET_STRATEGIES = {
    "lsb": get_data_in_LSB
}

flags = {
    "encrypt": False,
    "decrypt": False,
    "password": False,
    "output_path": "./out",
    "verbose": False,
}


def setup_logger():
    # create logger
    logger = logging.getLogger('steganography')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


# TODO: Add flags for strategy selection
# TODO: Remove unnecessary png files from resources.
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("carry", help="path to carry image")
    parser.add_argument("secret", help="path to secret file to hide")
    parser.add_argument("-d", "--decrypt", help="retrieve hidden data from image", action='store_true')
    parser.add_argument("-o", "--output", help="path to store program output")
    parser.add_argument("-p", "--passcode", help="passcode to encrypt data")
    args = parser.parse_args()
    st = Steganography()
    if args.passcode:
        st.set_passcode(args.passcode)
    if not args.decrypt:
        st.set_output_path(args.output)
        st.hide_data(args.carry, args.secret, hide_data_in_LSB)
    else:
        st.set_output_path(args.secret)
        st.get_data(args.carry, get_data_in_LSB)


def run():
    setup_logger()
    parse_args()


class Steganography:

    def __init__(self):
        self.path_to_output = "./output.png"
        self.passcode = ''

    def set_output_path(self, path_to_output):
        self.path_to_output = path_to_output

    def set_passcode(self, passcode):
        self.passcode = passcode

    def hide_data(self, path_to_carry, path_to_secret, strategy):
        st = Steganographer(path_to_carry)
        # passcode = ''  # TODO: get passcode from stdin
        st.hide_data_from_file(path=path_to_secret, out_path=self.path_to_output, strategy=strategy, passcode=self.passcode)

    def get_data(self, path_to_carry, strategy):
        # passcode = ''  # TODO: get passcode from stdin
        Steganographer.get_data_from_image(image_path=path_to_carry, out_path=self.path_to_output, strategy=strategy, passcode=self.passcode)