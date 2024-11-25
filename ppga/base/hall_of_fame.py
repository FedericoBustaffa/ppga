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
        buf = ""
        for i, ind in enumerate(self.hof):
            buf += f"{i+1}. {str(ind.fitness)}\n"

        return buf

    def update(self, population: list[Individual]):
        print("---------- Before HOF -------")
        self.hof.extend(population)
        for i in self.hof:
            print(i)

        self.hof = sorted([i for i in set(self.hof) if i.fitness != np.nan])[
            : self.size
        ]

        print("---------- After HOF -------")
        for i in self.hof:
            print(i)

    def clear(self):
        self.hof.clear()
