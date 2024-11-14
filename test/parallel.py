import random

from ppga import base, log


def crossover(
    toolbox: base.ToolBox, chosen: list[base.Individual], cxpb: float
) -> list[base.Individual]:
    offsprings = []
    for i in range(0, len(chosen), 2):
        offspring1, offspring2 = chosen[i], chosen[i + 1]
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(offspring1, offspring2)

        offsprings.extend([offspring1, offspring2])

    return offsprings


def mutation(
    toolbox: base.ToolBox, offsprings: list[base.Individual], mutpb: float
) -> list[base.Individual]:
    for i, o in enumerate(offsprings):
        if random.random() <= mutpb:
            offsprings[i] = toolbox.mutate(o)

    return offsprings


def evaluate(
    toolbox: base.ToolBox, offsprings: list[base.Individual]
) -> list[base.Individual]:
    for i, o in enumerate(offsprings):
        offsprings[i] = toolbox.evaluate(o)

    return offsprings


def run(
    toolbox: base.ToolBox,
    n: int,
    keep: float,
    cxpb: float,
    mutpb: float,
    generations: int,
    hof: base.HallOfFame,
    log_level: str | int = log.INFO,
) -> list[base.Individual]:
    population = toolbox.generate(n)

    for g in range(generations):
        chosen = toolbox.select(population, n)
        offsprings = crossover(toolbox, chosen, cxpb)
        offsprings = mutation(toolbox, offsprings, mutpb)
        offsprings = evaluate(toolbox, offsprings)
        population = toolbox.replace(population, offsprings)

        hof.update(population)

    return population
