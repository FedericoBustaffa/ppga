import copy
from functools import partial
from typing import Callable

import numpy as np

from ppga import base


class ToolBox:
    def __init__(self) -> None:
        self.clone_func = copy.deepcopy

    def set_clone(self, func, *args, **kwargs) -> None:
        self.clone_func = partial(func, *args, **kwargs)

    def clone(self, individual: base.Individual) -> base.Individual:
        return self.clone_func(individual)

    def set_weights(self, weights: tuple) -> None:
        self.weights = weights

    def set_generation(self, func: Callable, *args, **kwargs) -> None:
        self.generation_func = partial(func, *args, **kwargs)

    def generate(self, population_size: int) -> base.Population:
        chromosomes = np.array([self.generation_func() for _ in range(population_size)])
        return base.Population(chromosomes)

    def set_selection(self, func: Callable, *args, **kwargs) -> None:
        self.selection_func = func
        self.selection_args = args
        self.selection_kwargs = kwargs

    def select(
        self, population: base.Population, population_size: int
    ) -> base.Population:
        selected = self.selection_func(
            population.individuals,
            population_size,
            *self.selection_args,
            **self.selection_kwargs,
        )
        population.subst(selected)

        return population

    def set_crossover(self, func: Callable, *args, **kwargs) -> None:
        self.crossover_func = func
        self.crossover_args = args
        self.crossover_kwargs = kwargs

    def crossover(
        self, father: np.ndarray, mother: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        offspring1, offspring2 = self.crossover_func(
            father,
            mother,
            *self.crossover_args,
            **self.crossover_kwargs,
        )

        return offspring1, offspring2

    def set_mutation(self, func: Callable, *args, **kwargs) -> None:
        self.mutation_func = func
        self.mutation_args = args
        self.mutation_kwargs = kwargs

    def mutate(self, chromosome: np.ndarray) -> np.ndarray:
        chromosome = self.mutation_func(
            chromosome, *self.mutation_args, **self.mutation_kwargs
        )

        return chromosome

    def set_evaluation(self, func: Callable, *args, **kwargs) -> None:
        self.evaluation_func = func
        self.evaluation_args = args
        self.evaluation_kwargs = kwargs

    def evaluate(self, chromosome: np.ndarray) -> float:
        values = self.evaluation_func(
            chromosome, *self.evaluation_args, **self.evaluation_kwargs
        )

        fitness = sum([v * w for v, w in zip(values, self.weights)])

        return fitness
