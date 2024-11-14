import random

from ppga.base import Individual, ToolBox


def reproduction(
    chosen: list[Individual], toolbox: ToolBox, cxpb: float, mutpb: float
) -> list[Individual]:
    offsprings = []
    for i in range(0, len(chosen), 2):
        father, mother = random.choices(chosen, k=2)
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(father, mother)

            if random.random() <= mutpb:
                offspring1 = toolbox.mutate(offspring1)

            if random.random() <= mutpb:
                offspring2 = toolbox.mutate(offspring2)

            offsprings.extend([offspring1, offspring2])
        else:
            offsprings.extend([toolbox.clone(father), toolbox.clone(mother)])

    return offsprings
