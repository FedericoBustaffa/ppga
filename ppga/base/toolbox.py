import copy
from functools import partial
from typing import Callable

import numpy as np

from ppga.base.individual import Individual


class ToolBox:
    def clone(self, individual: Individual) -> Individual:
        return copy.deepcopy(individual)

    def set_weights(self, weights: tuple) -> None:
        self.weights = weights

    def set_generation(self, func: Callable, *args, **kwargs) -> None:
        self.generation_func = partial(func, *args, **kwargs)

    def generate(self, population_size: int) -> list[Individual]:
        population = [self.generation_func() for _ in range(population_size)]
        return [Individual(i) for i in population]

    def set_selection(self, func: Callable, *args, **kwargs) -> None:
        self.selection_func = func
        self.selection_args = args
        self.selection_kwargs = kwargs

    def select(
        self, population: list[Individual], population_size: int
    ) -> list[Individual]:
        return self.selection_func(
            population, population_size, *self.selection_args, **self.selection_kwargs
        )

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

    def evaluate(self, chromosome: np.ndarray) -> tuple[tuple, float]:
        values = self.evaluation_func(
            chromosome, *self.evaluation_args, **self.evaluation_kwargs
        )

        fitness = sum([v * w for v, w in zip(values, self.weights)])

        return (values, fitness)

    def set_replacement(self, func: Callable, *args, **kwargs) -> None:
        self.replacement_func = func
        self.replacement_args = args
        self.replacement_kwargs = kwargs

    def replace(
        self, population: list[Individual], offsprings: list[Individual]
    ) -> list[Individual]:
        return self.replacement_func(
            population, offsprings, *self.replacement_args, **self.replacement_kwargs
        )
