import random

from ppga.base import Individual, ToolBox


def crossover(
    population: list[Individual], toolbox: ToolBox, cxpb: float
) -> list[Individual]:
    offsprings = []
    for i in range(0, len(population), 2):
        offspring1, offspring2 = random.choices(population, k=2)
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(offspring1, offspring2)

        offsprings.extend([toolbox.clone(offspring1), toolbox.clone(offspring2)])

    return offsprings


def mutation(
    population: list[Individual], toolbox: ToolBox, mutpb: float
) -> list[Individual]:
    for i, ind in enumerate(population):
        if random.random() <= mutpb:
            population[i] = toolbox.mutate(ind)

    return population


def evaluation(population: list[Individual], toolbox: ToolBox) -> None:
    for i, ind in enumerate(population):
        population[i] = toolbox.evaluate(ind)


def reproduction(
    population: list[Individual], toolbox: ToolBox, cxpb: float, mutpb: float
) -> list[Individual]:
    offsprings = crossover(population, toolbox, cxpb)
    offsprings = mutation(population, toolbox, cxpb)

    return offsprings
