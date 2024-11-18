import random


def gen_repetition(values, length: int):
    return random.choices(values, k=length)


def gen_permutation(values):
    return random.sample(values, k=len(values))
