from ppga.base import Individual


def elitist(
    population: list[Individual], offsprings: list[Individual], keep: float
) -> list[Individual]:
    """Try to keep the specified percentage of the old generation"""
    assert keep >= 0 and keep <= 1.0
    if keep == 0.0:
        return offsprings

    n = round(len(population) * keep)
    to_keep = sorted(population, reverse=True)[:n]

    return to_keep + offsprings
