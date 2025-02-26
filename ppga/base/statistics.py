import numpy as np

from ppga.base.individual import Individual


class Statistics:
    def __init__(self) -> None:
        self.max = []
        self.mean = []
        self.min = []

        self.diversity = []
        self.evals = []

        # keep track of the parallel time
        self.times = []

    def update(self, population: list[Individual]) -> None:
        scores = np.array([i.fitness for i in population])
        scores = scores[~np.isinf(scores)]

        # update the fitness trend
        self.max.append(np.max(scores) if len(scores) != 0 else np.nan)
        self.mean.append(np.mean(scores) if len(scores) != 0 else np.nan)
        self.min.append(np.min(scores) if len(scores) != 0 else np.nan)

        # update the biodiversity
        uniques = set(population)
        self.diversity.append(len(uniques) / len(population))

    def update_evals(self, evals_num: int) -> None:
        self.evals.append(evals_num)

    def update_time(self, time: float) -> None:
        self.times.append(time)

    def to_dict(self) -> dict[str, list]:
        return {
            "evals": self.evals,
            "max": self.max,
            "mean": self.mean,
            "min": self.min,
            "diversity": self.diversity,
            "time": self.times,
        }
