from tqdm import tqdm

from ppga import log
from ppga.algorithms import batch
from ppga.base import HallOfFame, Individual, Statistics, ToolBox
from ppga.parallel import Pool


def custom(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.1,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
    workers_num: int = 0,
):
    stats = Statistics()
    logger = log.getCoreLogger()

    # only use the physical cores
    pool = Pool(workers_num, logical=False) if workers_num != 0 else None
    if pool is not None:
        toolbox.set_map(pool.map, toolbox, cxpb, mutpb)

    # generate the initial population
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")

    for g in tqdm(range(max_generations), ncols=80, ascii=True):
        selected = toolbox.select(population, population_size)
        logger.debug(f"selected individuals: {len(selected)}")

        couples = batch.mating(selected)
        logger.debug(f"couples generated: {len(couples)}")

        # pool map
        offsprings = toolbox.map(batch.cx_mut_eval, iterable=couples)
        offsprings_copy = []
        for couple in offsprings:
            if couple != ():
                offsprings_copy.extend(couple)

        logger.debug(f"{len(offsprings_copy)} new individuals generated")

        # perform a total replacement
        population = toolbox.replace(population, offsprings_copy)
        logger.debug(f"population size: {len(population)}")

        if hall_of_fame is not None:
            hall_of_fame.update(offsprings_copy)
            logger.debug(f"hall of fame size: {len(hall_of_fame)}")

        stats.update(population)
        stats.update_evals(len(offsprings))

    if pool is not None:
        pool.join()

    return population, stats
