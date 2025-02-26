import numpy as np

from ppga import base


class Population:
    def __init__(self, chromosomes: np.ndarray):
        self.chromosomes = chromosomes
        self.scores = np.array([0.0 for _ in range(len(chromosomes))])
        self.individuals = [
            base.Individual(chromosomes) for _ in range(len(chromosomes))
        ]

    @property
    def size(self) -> int:
        return len(self.scores)

    def __iter__(self):
        return iter(self.individuals)

    def __next__(self):
        return next(iter(self.individuals))
