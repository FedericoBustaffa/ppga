import random

from ppga.base.individual import Individual


def sel_truncation(population: list[Individual], k: int) -> list[Individual]:
    return sorted(population, reverse=True)[:k]


def sel_tournament(
    population: list[Individual], k: int, tournsize: int = 2
) -> list[Individual]:
    selected = []

    for _ in range(k):
        aspirants = random.sample(population, k=tournsize)
        winner = max(aspirants)
        selected.append(winner)

    return selected


def sel_roulette(population: list[Individual], k: int) -> list[Individual]:
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


def sel_ranking(population: list[Individual], k: int) -> list[Individual]:
    population = sorted(population)
    total = sum([i for i in range(len(population))])
    ranks = [i / total for i in range(len(population))]

    return random.choices(population, weights=ranks, k=k)
