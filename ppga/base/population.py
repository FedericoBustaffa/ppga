import numpy as np

from ppga import base


class Population:
    def __init__(self, chromosomes: np.ndarray):
        self.chromosomes = chromosomes
        self.scores = np.array([0.0 for _ in range(len(chromosomes))])
        self.individuals = [
            base.Individual(chromosomes[i], fitness=self.scores[i])
            for i in range(len(chromosomes))
        ]

    def update(self):
        for i, ind in enumerate(self.individuals):
            ind.fitness = self.scores[i]

    def __len__(self) -> int:
        return len(self.scores)

    def __iter__(self):
        return iter(self.individuals)

    def __next__(self):
        return next(iter(self.individuals))
