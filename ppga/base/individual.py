import json
import sys
from typing import Any

import numpy as np


class Individual:
    def __init__(self, chromosome) -> None:
        self.chromosome = chromosome

        # always converts the chromosome structure to a list
        if not isinstance(self.chromosome, np.ndarray):
            self.chromosome = np.array(self.chromosome)

        self.values = ()
        self.fitness = 0.0
        self.valid = False

    def __hash__(self) -> int:
        return hash(tuple(self.chromosome))

    def __repr__(self) -> str:
        dict_repr = self.__dict__
        dict_repr["chromosome"] = dict_repr["chromosome"].tolist()
        dict_repr["values"] = tuple(dict_repr["values"])
        dict_repr["fitness"] = float(dict_repr["fitness"])

        return json.dumps(dict_repr, indent=2)

    def __eq__(self, other) -> bool:
        assert isinstance(other, Individual)
        return np.array_equal(self.chromosome, other.chromosome)

    def __lt__(self, other) -> bool:
        assert isinstance(other, Individual)
        if not self.valid:
            return True
        elif not other.valid:
            return False
        return self.fitness < other.fitness

    def __le__(self, other) -> bool:
        assert isinstance(other, Individual)
        if not self.valid:
            return True
        elif not other.valid:
            return False
        return self.fitness <= other.fitness

    def __gt__(self, other) -> bool:
        assert isinstance(other, Individual)
        if not self.valid:
            return False
        elif not other.valid:
            return True
        return self.fitness > other.fitness

    def __ge__(self, other) -> bool:
        assert isinstance(other, Individual)
        if not self.valid:
            return False
        elif not other.valid:
            return True
        return self.fitness >= other.fitness

    def __sizeof__(self) -> int:
        return (
            sys.getsizeof(self.chromosome)
            + sys.getsizeof(self.fitness)
            + sys.getsizeof(self.values)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "chromsome": self.chromosome.tolist(),
            "values": self.values,
            "fitness": self.fitness,
        }
