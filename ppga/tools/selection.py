import random

from ppga import base


def sel_truncation(population: base.Population, k: int) -> list[base.Individual]:
    return list(sorted(population.individuals, reverse=True))[:k]


def sel_tournament(
    population: list[base.Individual], k: int, tournsize: int = 2
) -> list[base.Individual]:
    selected = []
    for _ in range(k):
        winner = max(random.sample(population, k=tournsize))
        selected.append(winner)

    return selected


def sel_roulette(population: base.Population, k: int) -> base.Population:
    total = 0.0
    for i in population:
        if i.fitness < 0.0:
            total -= 1.0 / i.fitness
        else:
            total += i.fitness

    if total == 0.0:
        return random.choices(population, k=k)
    else:
        normalized_scores = []
        for i in population:
            if i.fitness < 0.0:
                normalized_scores.append(-1.0 / i.fitness / total)
            else:
                normalized_scores.append(i.fitness / total)

        return random.choices(population, k=k, weights=normalized_scores)


def sel_ranking(population: base.Population, k: int) -> base.Population:
    population = sorted(population)
    total = sum([i for i in range(len(population))])
    ranks = [i / total for i in range(len(population))]

    return random.choices(population, weights=ranks, k=k)
