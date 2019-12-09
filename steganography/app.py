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

LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def setup_logger(level):
    # create logger
    logger = logging.getLogger('steganography')
    logger.setLevel(level)

    # create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(level=level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


# TODO: Add flags for strategy selection
# TODO: Remove unnecessary png files from resources.
def parse_args():
    parser = argparse.ArgumentParser(prog='steganography')
    parser.add_argument('--log-level', help='set logging level', choices=['debug', 'info', 'warn', 'error', 'critical'],
                        default='info')
    subparsers = parser.add_subparsers(help='help for subcommand', required=True, dest='subcommand')

    # create parser for hide
    parser_hide = subparsers.add_parser('hide', help='hide help')
    parser_hide.add_argument('image', help='image to hide data in')
    parser_hide.add_argument('data', help='data to hide')
    parser_hide.add_argument('-o', '--output', help='path to store output image', default='./out.png')
    parser_hide.add_argument('-e', '--encrypt', help='encrypt data',  action='store_true', default=False)
    parser_hide.add_argument('-c', '--compression', help='compress data',  action='store_true', default=False)

    # create parser for get
    parser_get = subparsers.add_parser('get', help='get help')
    parser_get.add_argument('image', help='image to get data from')
    parser_get.add_argument('-o', '--output', help='path to store output data', default='./out')
    parser_get.add_argument('-d', '--decrypt', help='decrypt data',  action='store_true', default=False)
    parser_get.add_argument('-c', '--compression', help='decompress data',  action='store_true', default=False)

    args = parser.parse_args()

    return args


def run():
    args = parse_args()
    setup_logger(LOG_LEVELS[args.log_level])

    log = logging.getLogger('steganography')
