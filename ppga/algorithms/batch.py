import random

import numpy as np

from ppga import base


def mating(population: list[base.Individual]) -> np.ndarray:
    couples = []
    for i in range(0, len(population), 2):
        couples.append((population[i].chromosome, population[i + 1].chromosome))

    return np.asarray(couples)


def crossover(couples: np.ndarray, toolbox: base.ToolBox, cxpb: float) -> np.ndarray:
    offsprings = []
    for father, mother in couples:
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(father, mother)

            offsprings.extend([offspring1, offspring2])

    return np.asarray(offsprings)


def mutation(population: np.ndarray, toolbox: base.ToolBox, mutpb: float) -> np.ndarray:
    for i, ind in enumerate(population):
        if random.random() <= mutpb:
            population[i] = toolbox.mutate(ind)

    return population


def evaluation(population: np.ndarray, toolbox: base.ToolBox) -> list:
    scores = []
    for i, ind in enumerate(population):
        scores.append(toolbox.evaluate(ind))

    return scores


def cx_mut_eval(
    couple: np.ndarray, toolbox: base.ToolBox, cxpb: float, mutpb: float
) -> tuple:
    father, mother = couple
    if random.random() <= cxpb:
        offspring1, offspring2 = toolbox.crossover(father, mother)

        if random.random() <= mutpb:
            offspring1 = toolbox.mutate(offspring1)

        if random.random() <= mutpb:
            offspring2 = toolbox.mutate(offspring2)

        values1, fitness1 = toolbox.evaluate(offspring1)
        values2, fitness2 = toolbox.evaluate(offspring2)

        return (
            base.Individual(offspring1, values1, fitness1),
            base.Individual(offspring2, values2, fitness2),
        )

    return ()
