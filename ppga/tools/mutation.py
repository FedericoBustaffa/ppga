import numpy as np
from numpy import random


def mut_bitflip(chromosome: np.ndarray, indpb: float = 0.5):
    probs = random.random(chromosome.shape)
    chromosome[probs <= indpb] = ~chromosome[probs <= indpb]

    return chromosome


def mut_swap(chromosome: np.ndarray, indpb: float = 0.5):
    for i, gene in enumerate(chromosome):
        if random.random() < indpb:
            new_pos = random.randint(0, len(chromosome))
            while i == new_pos:
                new_pos = random.randint(0, len(chromosome))
            chromosome[i], chromosome[new_pos] = chromosome[new_pos], chromosome[i]

    return chromosome


def mut_rotation(chromosome: np.ndarray):
    a, b = random.choice([i for i in range(len(chromosome) + 1)], size=2, replace=False)
    if a > b:
        a, b = b, a
    chromosome[a:b] = np.flip(chromosome[a:b])

    return chromosome


def mut_normal(
    chromosome: np.ndarray, mu: np.ndarray, sigma: np.ndarray, indpb: float = 0.5
) -> np.ndarray:
    probs = random.random(chromosome.shape)
    mutations = random.normal(loc=mu, scale=sigma, size=chromosome.shape)
    chromosome[probs <= indpb] = mutations[probs <= indpb]

    return chromosome
