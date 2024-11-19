import logging
import multiprocessing as mp
import random
import sys
import time

from knapsack import Item, evaluate

from ppga import base, log, parallel, tools
from ppga.algorithms import batch


def ptask(couples, toolbox):
    logger = log.getUserLogger()

    # crossover
    offsprings = []
    for father, mother in couples:
        if random.random() <= 0.8:
            start = time.perf_counter()
            offspring1, offspring2 = toolbox.crossover(father, mother)
            offsprings.extend([toolbox.clone(offspring1), toolbox.clone(offspring2)])
            cx_time = time.perf_counter() - start
            logger.log(25, f"{mp.current_process().name} crossover: {cx_time} seconds")

    # mutation
    for i, ind in enumerate(offsprings):
        if random.random() <= 0.2:
            start = time.perf_counter()
            offsprings[i] = toolbox.mutate(ind)
            mut_time = time.perf_counter() - start
            logger.log(25, f"{mp.current_process().name} mutation: {mut_time} seconds")

    # evaluation
    for i, ind in enumerate(offsprings):
        start = time.perf_counter()
        offsprings[i] = toolbox.evaluate(ind)
        eval_time = time.perf_counter() - start
        logger.log(25, f"{mp.current_process().name} evaluation: {eval_time} seconds")

    return offsprings


def parallel_run(toolbox: base.ToolBox, pop_size: int, max_gens: int):
    logger = log.getUserLogger()

    pool = parallel.Pool()

    # generation
    start = time.perf_counter()
    population = toolbox.generate(pop_size)
    gen_time = time.perf_counter() - start
    logger.log(25, f"generation: {gen_time} seconds")

    for g in range(max_gens):
        # selection
        start = time.perf_counter()
        selected = toolbox.select(population, pop_size)
        sel_time = time.perf_counter() - start
        logger.log(25, f"selection: {sel_time} seconds")

        # mating
        couples = batch.mating(selected)

        # parallel crossover, mutation and evaluation
        start = time.perf_counter()
        offsprings = pool.map(ptask, couples, args=[toolbox])
        parallel_time = time.perf_counter() - start
        logger.log(25, f"parallel: {parallel_time} seconds")

        # replacement
        start = time.perf_counter()
        population = toolbox.replace(population, offsprings)
        replace_time = time.perf_counter() - start
        logger.log(25, f"replacement: {replace_time} seconds")

    pool.join()


def main(argv: list[str]) -> None:
    if len(argv) != 4:
        print(f"USAGE: py {argv[0]} <Items> <N> <G>")
        exit(1)

    logger = log.getUserLogger()
    logger.setLevel(logging.INFO)

    items_num = int(argv[1])

    items = [Item(random.random(), random.random()) for _ in range(items_num)]
    capacity = sum([i.weight for i in items]) * 0.7

    toolbox = base.ToolBox()
    toolbox.set_weights(weights=(3.0, -1.0))
    toolbox.set_generation(tools.gen_repetition, (0, 1), len(items))
    toolbox.set_selection(tools.sel_ranking)
    toolbox.set_crossover(tools.cx_uniform)
    toolbox.set_mutation(tools.mut_bitflip)
    toolbox.set_evaluation(evaluate, items, capacity)
    toolbox.set_replacement(tools.elitist, keep=0.3)

    start = time.perf_counter()
    parallel_run(toolbox, int(argv[2]), int(argv[3]))
    ptime = time.perf_counter() - start
    logger.log(25, f"ptime: {ptime} seconds")


if __name__ == "__main__":
    main(sys.argv)