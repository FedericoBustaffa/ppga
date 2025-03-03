import time

import numpy as np
from tqdm import tqdm

from ppga import base, log, parallel, tools


def simple(
    toolbox: base.ToolBox,
    population_size: int,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | tools.HallOfFame = None,
    workers_num: int = 0,
) -> tuple[base.Population, tools.Statistics]:
    logger = log.getCoreLogger()
    stats = tools.Statistics()

    # generate the initial population
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")
    for i, ind in enumerate(population):
        logger.debug(
            f"{ind.chromosome} : {population.chromosomes[i]} - {np.array_equal(ind.chromosome, population.chromosomes[i])}"
        )

    parallel.create_shm(population)
    pool = parallel.Pool(population, toolbox, cxpb, mutpb, workers_num)

    for g in tqdm(range(max_generations), ncols=80, ascii=True):
        population = toolbox.select(population, population_size)
        for i, ind in enumerate(population):
            logger.debug(
                f"{ind.chromosome} : {population.chromosomes[i]} - {np.array_equal(ind.chromosome, population.chromosomes[i])}"
            )
        logger.debug(f"selected individuals: {len(population)}")

        # parallel crossover, mutation and evaluation
        start = time.perf_counter()
        pool.cx_mut_eval(population)
        end = time.perf_counter()
        logger.debug(f"{len(population)} new individuals generated")

        population.update()
        stats.update_time(end - start)
        stats.update(population.individuals)
        stats.update_evals(len(population))

        if hall_of_fame is not None:
            hall_of_fame.update(population.individuals)
            logger.debug(f"hall of fame size: {len(hall_of_fame)}")

    parallel.free_shm()
    pool.join()

    return population, stats
