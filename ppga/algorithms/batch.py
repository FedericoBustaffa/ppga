import random

from ppga import log
from ppga.base import Individual, ToolBox

logger = log.getCoreLogger(log.DEBUG)


def mating(population: list[Individual]) -> list[tuple[Individual, Individual]]:
    couples = []
    for i in range(0, len(population), 2):
        couples.append((population[i], population[i + 1]))

    return couples


def crossover(
    couples: list[tuple[Individual, Individual]], toolbox: ToolBox, cxpb: float
) -> list[Individual]:
    offsprings = []
    for father, mother in couples:
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(father, mother)
            offsprings.extend([toolbox.clone(offspring1), toolbox.clone(offspring2)])

    return offsprings


def mutation(
    population: list[Individual], toolbox: ToolBox, mutpb: float
) -> list[Individual]:
    for i, ind in enumerate(population):
        if random.random() <= mutpb:
            population[i] = toolbox.mutate(ind)

    return population


def evaluation(population: list[Individual], toolbox: ToolBox) -> list[Individual]:
    for i, ind in enumerate(population):
        if not ind.valid:
            population[i] = toolbox.evaluate(ind)

    return population


def cx_mut_eval(couples, toolbox, cxpb, mutpb):
    offsprings = crossover(couples, toolbox, cxpb)
    offsprings = mutation(offsprings, toolbox, mutpb)
    offsprings = evaluation(offsprings, toolbox)

    return offsprings
