import numpy as np

from ppga import base


class Population:
    def __init__(self, chromosomes: np.ndarray):
        self.chromosomes = chromosomes
        self.scores = np.array([0.0 for _ in range(len(chromosomes))])
        self.individuals = [
            base.Individual(chromosomes[i].copy(), fitness=self.scores[i])
            for i in range(len(chromosomes))
        ]

    def update(self):
        for i in range(len(self.individuals)):
            self.individuals[i].fitness = self.scores[i]

    def subst(self, individuals: list[base.Individual]):
        self.individuals = individuals
        for i in range(len(individuals)):
            self.chromosomes[i][:] = individuals[i].chromosome[:]
            self.scores[i] = self.individuals[i].fitness

    def __len__(self) -> int:
        return len(self.scores)

    def __iter__(self):
        return iter(self.individuals)

    def __next__(self):
        return next(iter(self.individuals))
