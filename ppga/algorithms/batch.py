import random

import numpy as np

from ppga import base


def mating(population: list[base.Individual]) -> np.ndarray:
    couples = []
    for i in range(0, len(population), 2):
        couples.append((population[i].chromosome, population[i + 1].chromosome))

    return np.asarray(couples)


def crossover(chromosomes: np.ndarray, toolbox: base.ToolBox, cxpb: float):
    for i in range(0, len(chromosomes) - 1, 2):
        if random.random() <= cxpb:
            chromosomes[i][:], chromosomes[i + 1][:] = toolbox.crossover(
                chromosomes[i], chromosomes[i + 1]
            )


def mutation(chromosomes: np.ndarray, toolbox: base.ToolBox, mutpb: float):
    for i, ind in enumerate(chromosomes):
        if random.random() <= mutpb:
            chromosomes[i][:] = toolbox.mutate(ind)


def evaluation(population: np.ndarray, scores: np.ndarray, toolbox: base.ToolBox):
    for i, ind in enumerate(population):
        scores[i] = toolbox.evaluate(ind)
