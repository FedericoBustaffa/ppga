import numpy as np
from numpy import random


def gen_repetition(values, length: int):
    return random.choice(values, size=length)


def gen_permutation(values) -> np.ndarray:
    return random.permutation(values)
