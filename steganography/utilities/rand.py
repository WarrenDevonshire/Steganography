import numpy as np
from numpy import random


def get_random_sequence(lower_bound, upper_bound, seed):
    # TODO: Write function documentation
    sequence = np.arange(lower_bound, upper_bound)
    random.seed(seed)
    random.shuffle(sequence)
    return sequence
