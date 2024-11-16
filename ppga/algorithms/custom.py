import numpy as np
import psutil

from ppga import log
from ppga.algorithms import batch
from ppga.base import HallOfFame, Statistics, ToolBox
from ppga.parallel import Pool, Worker


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
        couples = batch.mating(chosen)

        # perform crossover
        offsprings = batch.crossover(couples, toolbox, cxpb)

        # # perform mutation
        offsprings = batch.mutation(offsprings, toolbox, mutpb)

        # # evaluate offsprings
        offsprings = batch.evaluation(offsprings, toolbox)
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

    pool = Pool(False, log_level)

    # only use the physical cores
    population = toolbox.generate(population_size)

    logger.info(f"\t{'gen':15s}{'mean evals/worker':15s}")
    offsprings = []
    for g in range(max_generations):
        chosen = toolbox.select(population, population_size)

        couples = batch.mating(chosen)

        # new API
        offsprings = pool.map(batch.cx_mut_eval, couples, toolbox, cxpb, mutpb)

        # perform a total replacement
        population = toolbox.replace(population, offsprings)

        stats.update(population)
        logger.info(f"\t{g:<15d}{np.mean(len(offsprings)):<15f}")

        if hall_of_fame is not None:
            hall_of_fame.update(population)

    pool.join()

    return population, stats
