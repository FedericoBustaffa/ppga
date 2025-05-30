import time
from functools import partial
from itertools import chain

from tqdm import tqdm

from ppga import base, log, parallel, tools
from ppga.algorithms import batch


def simple(
    toolbox: base.ToolBox,
    population_size: int,
    keep: float = 0.1,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | base.HallOfFame = None,
    workers_num: int = 0,
):
    stats = base.Statistics()
    logger = log.getCoreLogger()

    map_func = map
    cx_mut_eval = partial(
        batch.cx_mut_eval,
        toolbox=toolbox,
        cxpb=cxpb,
        mutpb=mutpb,
    )

    # only use the physical cores
    pool = parallel.Pool(workers_num) if workers_num > 1 or workers_num < 0 else None
    if pool is not None:
        map_func = pool.map

    toolbox.set_replacement(tools.elitist, keep=keep)

    # generate the initial population
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")

    for g in tqdm(range(max_generations), ncols=80, ascii=True):
        selected = toolbox.select(population, population_size)
        logger.debug(f"selected individuals: {len(selected)}")

        # create couples
        couples = batch.mating(selected)
        logger.debug(f"{len(couples)} couples generated")

        # perform crossover, mutation and evaluation
        start = time.perf_counter()
        offsprings = list(chain(*map_func(cx_mut_eval, couples)))
        end = time.perf_counter()
        stats.update_time(end - start)

        # update stats
        stats.update(offsprings)
        stats.update_evals(len(offsprings))
        logger.debug(f"{len(offsprings)} new individuals generated")

        # perform the replacement
        population = toolbox.replace(population, offsprings)
        logger.debug(f"population size: {len(population)}")

        # update hall of fame
        if hall_of_fame is not None:
            hall_of_fame.update(offsprings)
            logger.debug(f"hall of fame size: {len(hall_of_fame)}")

    if pool is not None:
        pool.join()

    return population, stats
