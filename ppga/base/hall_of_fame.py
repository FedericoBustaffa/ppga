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
        self.hof = sorted(list(set(self.hof + population)), reverse=True)[: self.size]

    def clear(self):
        self.hof.clear()
