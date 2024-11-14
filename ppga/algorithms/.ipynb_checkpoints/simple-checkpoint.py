import multiprocessing as mp
import os
import random
import time

from tqdm import tqdm

from ppga.algorithms.worker import Worker
from ppga.base import HallOfFame, Individual, Statistics, ToolBox


def reproduction(chosen: list[Individual], cxpb: float, mutpb: float, toolbox: ToolBox):
    offsprings = []
    for i in range(0, len(chosen) - 1, 1):
        if random.random() <= cxpb:
            offspring1, offspring2 = toolbox.crossover(chosen[i], chosen[i + 1])

            if random.random() <= mutpb:
                toolbox.mutate(offspring1)
        
            if random.random() <= mutpb:
                toolbox.mutate(offspring2)

            offsprings.extend([offspring1, offspring2])

    return offsprings


def sga(
    toolbox: ToolBox,
    population_size: int,
    cxpb: float,
    mutpb: float,
    max_generations: int,
    hall_of_fame: None | HallOfFame = None,
):
    stats = Statistics()
    worker_file = open(f"./results/{mp.current_process().name}.txt", "w")

    population = toolbox.generate(population_size)
    for g in tqdm(range(max_generations), desc="generations", ncols=80):
        chosen = toolbox.select(population, population_size)
        offsprings = reproduction(chosen, cxpb, mutpb, toolbox)

        for offspring in offsprings:
            start = time.perf_counter()
            offspring = toolbox.evaluate(offspring)
            eval_time = time.perf_counter() - start
            print(eval_time, file=worker_file)

        stats.update_evals(len(offsprings))

        population = toolbox.replace(population, offsprings)

        stats.update(population)

        if hall_of_fame is not None:
            hall_of_fame.update(population)

    worker_file.close()

    return population, stats


def psga(
    toolbox: ToolBox,
    population_size: int,
    cxpb: float,
    mutpb: float,
    max_generations: int,
    hall_of_fame: None | HallOfFame = None,
):
    stats = Statistics()

    workers_num = os.cpu_count()
    assert workers_num is not None

    workers = [Worker(toolbox, cxpb, mutpb) for _ in range(workers_num)]

    population = toolbox.generate(population_size)
    for g in tqdm(range(max_generations), desc="generations", ncols=80):
        chosen = toolbox.select(population, population_size)
        chunksize = len(chosen) // workers_num
        carry = len(chosen) % workers_num

        for i in range(carry):
            workers[i].send(chosen[i * chunksize : i * chunksize + chunksize + 1])

        for i in range(carry, workers_num, 1):
            workers[i].send(chosen[i * chunksize : i * chunksize + chunksize])

        # keep only the worst time for each worker
        offsprings = []
        evals = []
        for worker in workers:
            offsprings_chunk = worker.recv()
            offsprings.extend(offsprings_chunk)
            evals.append(len(offsprings_chunk))

        population = toolbox.replace(population, offsprings)

        stats.update(population)
        stats.update_multievals(evals)

        if hall_of_fame is not None:
            hall_of_fame.update(population)

    for w in workers:
        w.join()

    return population, stats
