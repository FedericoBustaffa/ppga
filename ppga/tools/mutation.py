import random

import numpy as np


def mut_bitflip(chromosome, indpb: float = 0.5):
    attr_type = type(chromosome[0])
    for i, gene in enumerate(chromosome):
        if random.random() < indpb:
            chromosome[i] = attr_type(not gene)

    return chromosome


def mut_swap(chromosome, indpb: float = 0.5):
    for i, gene in enumerate(chromosome):
        if random.random() < indpb:
            new_pos = random.randint(0, len(chromosome))
            while i == new_pos:
                new_pos = random.randint(0, len(chromosome))
            chromosome[i], chromosome[new_pos] = chromosome[new_pos], chromosome[i]

    return chromosome


def mut_rotation(chromosome):
    a, b = random.sample([i for i in range(len(chromosome) + 1)], k=2)
    if a > b:
        a, b = b, a
    chromosome[a:b] = np.flip(chromosome[a:b])

    return chromosome


def mut_gaussian(chromosome, sigma, alpha: float, indpb: float = 0.2):
    for i, x in enumerate(chromosome):
        if random.random() <= indpb:
            chromosome[i] = random.gauss(mu=x, sigma=sigma[i] * alpha)

    return chromosome
