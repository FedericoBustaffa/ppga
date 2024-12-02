import random

import numpy as np

from ppga.base import Individual, ToolBox


def mating(population: list[Individual]) -> np.ndarray:
    couples = []
    for i in range(0, len(population), 2):
        couples.append((population[i].chromosome, population[i + 1].chromosome))

    return np.asarray(couples)


def crossover(couples: np.ndarray, toolbox: ToolBox, cxpb: float) -> list[np.ndarray]:
    offsprings = []
    for father, mother in couples:
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(
                father.chromosome, mother.chromosome
            )
            offsprings.extend([offspring1, offspring2])

    return offsprings


def mutation(
    population: list[np.ndarray], toolbox: ToolBox, mutpb: float
) -> list[np.ndarray]:
    for i, ind in enumerate(population):
        if random.random() <= mutpb:
            population[i] = toolbox.mutate(ind)

    return population


def evaluation(population: list[np.ndarray], toolbox: ToolBox) -> list:
    scores = []
    for i, ind in enumerate(population):
        scores.append(toolbox.evaluate(ind))

    return scores


def cx_mut_eval(
    couples: np.ndarray, toolbox: ToolBox, cxpb: float, mutpb: float
) -> list[Individual]:
    offsprings = crossover(couples, toolbox, cxpb)
    offsprings = mutation(offsprings, toolbox, mutpb)
    values, scores = evaluation(offsprings, toolbox)

    offsprings = [Individual(i, v, s) for i, v, s in zip(offsprings, values, scores)]

    return offsprings
