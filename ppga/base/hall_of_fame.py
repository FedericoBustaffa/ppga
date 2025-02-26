import json

import numpy as np

from ppga.base.individual import Individual


class HallOfFame:
    def __init__(self, size: int):
        self.size = size
        self.hof = []

    def __getitem__(self, index: int) -> Individual:
        return self.hof[index]

    def __iter__(self):
        return iter(self.hof)

    def __next__(self):
        return next(iter(self.hof))

    def __len__(self) -> int:
        return len(self.hof)

    def __repr__(self) -> str:
        buf = []
        individual = {"chromosome": None, "values": (), "fitness": 0.0}
        for i, ind in enumerate(self.hof):
            individual["chromosome"] = ind.chromosome.tolist()
            individual["values"] = ind.values
            individual["fitness"] = ind.fitness
            buf.append(individual.copy())

        return json.dumps(buf, indent=2) + "\n"

    def update(self, population: list[Individual]):
        self.hof = sorted(
            [
                i
                for i in set(self.hof + population)
                if i.fitness != np.nan and i.fitness != 0.0
            ],
            reverse=True,
        )[: self.size]

    def clear(self):
        self.hof.clear()

    def to_list(self) -> list:
        return [i.to_dict() for i in self.hof]
