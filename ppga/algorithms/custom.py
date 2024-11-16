import numpy as np
import psutil

from ppga import log
from ppga.algorithms.utility import crossover, cx_mut_eval, evaluation, mating, mutation
from ppga.algorithms.worker import Worker
from ppga.base import HallOfFame, Statistics, ToolBox


def custom(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
    log_level: str | int = log.WARNING,
):
    stats = Statistics()
    logger = log.getCoreLogger(log_level)

    # generate the initial population
    population = toolbox.generate(population_size)

    logger.info(f"\t{'gen':15s}{'evals':15s}")
    for g in range(max_generations):
        # select individuals for reproduction
        chosen = toolbox.select(population, population_size)

        # create couples
        couples = mating(chosen)

        # perform crossover
        offsprings = crossover(couples, toolbox, cxpb)

        # # perform mutation
        offsprings = mutation(offsprings, toolbox, mutpb)

        # # evaluate offsprings
        offsprings = evaluation(offsprings, toolbox)
        evals = len(offsprings)

        # replace the old population
        population = toolbox.replace(population, offsprings)

        # update the Hall of Fame if present
        if hall_of_fame is not None:
            hall_of_fame.update(population)

        # update the stats
        stats.update(population)
        stats.update_evals(evals)

        # display current generation and number of evaluations
        logger.info(f"\t{g:<15d}{evals:<15d}")

    return population, stats


def pcustom(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
    log_level: str | int = log.WARNING,
):
    stats = Statistics()

    logger = log.getCoreLogger(log_level)

    # only use the physical cores
    workers_num = psutil.cpu_count(logical=False)
    assert workers_num is not None

    # dinamically resize the chunksize
    if population_size < workers_num:
        logger.warning(
            f"workers initialized: {population_size} out of {workers_num} cores"
        )
        workers_num = population_size

    chunksize = population_size // workers_num
    carry = population_size % workers_num

    handlers = [Worker(toolbox, cxpb, mutpb, log_level) for _ in range(workers_num)]
    for h in handlers:
        h.start()

    population = toolbox.generate(population_size)

    logger.info(f"\t{'gen':15s}{'mean evals/worker':15s}")
    offsprings = []
    for g in range(max_generations):
        chosen = toolbox.select(population, population_size)

        for i in range(carry):
            handlers[i].send(chosen[i * chunksize : i * chunksize + chunksize + 1])

        for i in range(carry, workers_num, 1):
            handlers[i].send(chosen[i * chunksize : i * chunksize + chunksize])

        offsprings.clear()
        evals = []
        for h in handlers:
            offsprings_chunk, worker_evals = h.recv()
            offsprings.extend(offsprings_chunk)
            evals.append(worker_evals)

        # perform a total replacement
        population = toolbox.replace(population, offsprings)

        stats.update(population)
        logger.info(f"\t{g:<15d}{np.mean(evals):<15f}")

        if hall_of_fame is not None:
            hall_of_fame.update(population)

    for h in handlers:
        h.join()

    return population, stats
