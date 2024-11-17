from tqdm import tqdm

from ppga import log
from ppga.algorithms import batch
from ppga.base import HallOfFame, Statistics, ToolBox
from ppga.parallel import Pool


def custom(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
):
    stats = Statistics()

    logger = log.getCoreLogger()

    # generate the initial population
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")

    for g in tqdm(range(max_generations), ncols=80):
        # select individuals for reproduction
        chosen = toolbox.select(population, population_size)
        logger.debug(f"selected individuals: {len(chosen)}")

        # create couples
        couples = batch.mating(chosen)
        logger.debug(f"couples generated: {len(couples)}")

        # perform crossover
        offsprings = batch.crossover(couples, toolbox, cxpb)
        logger.debug(f"offsprings generated: {len(offsprings)}")

        # # perform mutation
        offsprings = batch.mutation(offsprings, toolbox, mutpb)
        logger.debug(f"offsprings after mutation: {len(offsprings)}")

        # # evaluate offsprings
        offsprings = batch.evaluation(offsprings, toolbox)
        evals = len(offsprings)
        logger.debug(f"offsprings evaluated: {evals}")

        # replace the old population
        population = toolbox.replace(population, offsprings)
        logger.debug(f"population size: {len(population)}")

        # update the Hall of Fame if present
        if hall_of_fame is not None:
            hall_of_fame.update(population)

        # update the stats
        stats.update(population)
        stats.update_evals(evals)

    return population, stats


def pcustom(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
):
    stats = Statistics()

    logger = log.getCoreLogger()

    pool = Pool(False)

    # only use the physical cores
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")

    offsprings = []
    for g in tqdm(range(max_generations), ncols=80):
        chosen = toolbox.select(population, population_size)
        logger.debug(f"selected individuals: {len(chosen)}")

        couples = batch.mating(chosen)
        logger.debug(f"couples generated: {len(couples)}")

        # pool map
        offsprings = pool.map(
            func=batch.cx_mut_eval, iterable=couples, args=(toolbox, cxpb, mutpb)
        )
        logger.debug(f"offsprings generated: {len(offsprings)}")

        # perform a total replacement
        population = toolbox.replace(population, offsprings)
        logger.debug(f"population size: {len(population)}")

        stats.update(population)

        if hall_of_fame is not None:
            hall_of_fame.update(population)

    pool.join()

    return population, stats
