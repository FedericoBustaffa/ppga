import random

import numpy as np

from ppga import log, base

logger = log.getCoreLogger()


def mating(population: list[base.Individual]) -> np.ndarray:
    couples = []
    for i in range(0, len(population), 2):
        couples.append((population[i].chromosome,
                       population[i + 1].chromosome))

    return np.asarray(couples)


def crossover(couples: np.ndarray, toolbox: base.ToolBox, cxpb: float) -> np.ndarray:
    offsprings = []
    for father, mother in couples:
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(father, mother)
            # else:
            #     offspring1, offspring2 = toolbox.clone(
            #         father), toolbox.clone(mother)

            offsprings.extend([offspring1, offspring2])

    logger.info(f"{len(offsprings)} offsprings generated")

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

    logger.info(f"{len(population)} evaluated")

    return scores


def cx_mut_eval(
    couples: np.ndarray, toolbox: base.ToolBox, cxpb: float, mutpb: float
) -> list[base.Individual]:
    offsprings = crossover(couples, toolbox, cxpb)

    if len(offsprings) == 0:
        return []

    offsprings = mutation(offsprings, toolbox, mutpb)
    scores = evaluation(offsprings, toolbox)

    logger.debug(f"{len(offsprings)} new individuals generated")

    return [base.Individual(i, s[0], s[1]) for i, s in zip(offsprings, scores)]
