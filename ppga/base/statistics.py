from ppga.base.individual import Individual


class Statistics:
    def __init__(self) -> None:
        self.best = []
        self.mean = []
        self.worst = []

        self.diversity = []
        self.evals = []

    def update(self, population: list[Individual]) -> None:
        scores = [i.fitness for i in population]

        # update the fitness trend
        self.best.append(max(scores))
        self.mean.append(sum(scores) / len(scores))
        self.worst.append(min(scores))

        # update the biodiversity
        uniques = set(population)
        self.diversity.append(len(uniques) / len(population))

    def update_evals(self, evals_num: int) -> None:
        self.evals.append(evals_num)
