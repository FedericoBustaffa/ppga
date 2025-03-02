import time

# from functools import partial
# from itertools import chain
from tqdm import tqdm

from ppga import base, log, parallel

# from ppga.algorithms import batch

# def sequential_simple(
#     toolbox: base.ToolBox,
#     population_size: int,
#     cxpb: float = 0.8,
#     mutpb: float = 0.2,
#     max_generations: int = 50,
#     hall_of_fame: None | base.HallOfFame = None,
# ):
#     logger = log.getCoreLogger()
#     stats = base.Statistics()
#     map_func = map
#     cx_mut_eval = partial(batch.cx_mut_eval, toolbox=toolbox, cxpb=cxpb, mutpb=mutpb)

#     # generate the initial population
#     population = toolbox.generate(population_size)
#     logger.debug(f"generated individuals: {len(population)}")

#     for g in tqdm(range(max_generations), ncols=80, ascii=True):
#         selected = toolbox.select(population, population_size)
#         logger.debug(f"selected individuals: {len(selected)}")

#         couples = batch.mating(selected)
#         logger.debug(f"{len(couples)} couples generated")

#         # pool map
#         start = time.process_time()
#         offsprings = list(chain(*map_func(cx_mut_eval, couples)))
#         end = time.process_time()

#         stats.update_time(end - start)
#         logger.debug(f"{len(offsprings)} new individuals generated")
#         stats.update(offsprings)
#         stats.update_evals(len(offsprings))

#         # perform a total replacement
#         population = offsprings
#         logger.debug(f"population size: {len(population)}")

#         if hall_of_fame is not None:
#             hall_of_fame.update(offsprings)
#             logger.debug(f"hall of fame size: {len(hall_of_fame)}")

#     return population, stats


def simple(
    toolbox: base.ToolBox,
    population_size: int,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | base.HallOfFame = None,
    workers_num: int = 0,
) -> tuple[base.Population, base.Statistics]:
    # if workers_num == 0 or workers_num == 1:
    #     return sequential_simple(
    #         toolbox,
    #         population_size,
    #         cxpb,
    #         mutpb,
    #         max_generations,
    #         hall_of_fame,
    #     )

    logger = log.getCoreLogger()
    stats = base.Statistics()

    # generate the initial population
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")
    for ind in population:
        logger.debug(f"{ind.chromosome}")

    parallel.create_shm(population)
    pool = parallel.Pool(population, toolbox, cxpb, mutpb, workers_num)

    for g in tqdm(range(max_generations), ncols=80, ascii=True):
        population = toolbox.select(population, population_size)
        for ind in population:
            logger.debug(f"{ind.chromosome}")
        logger.debug(f"selected individuals: {len(population)}")

        # parallel work
        start = time.perf_counter()
        parallel.copy_to_shm(population)
        pool.cx_mut_eval(population)
        parallel.copy_from_shm(population)
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
