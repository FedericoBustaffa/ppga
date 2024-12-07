from tqdm import tqdm

from ppga import log
from ppga.algorithms import batch
from ppga.base import HallOfFame, Individual, Statistics, ToolBox
from ppga.parallel import Pool


def custom(
    toolbox: ToolBox,
    population_size: int,
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

    for g in tqdm(range(max_generations), ncols=80, ascii=True):
        # select individuals for reproduction
        selected = toolbox.select(population, population_size)
        logger.debug(f"selected individuals: {len(selected)}")

        # create couples
        couples = batch.mating(selected)
        logger.debug(f"couples generated: {len(couples)}")

        # perform crossover
        offsprings = batch.crossover(couples, toolbox, cxpb)
        logger.debug(f"offsprings generated: {len(offsprings)}")

        # # perform mutation
        offsprings = batch.mutation(offsprings, toolbox, mutpb)
        logger.debug(f"offsprings after mutation: {len(offsprings)}")

        # # evaluate offsprings
        scores = batch.evaluation(offsprings, toolbox)
        evals = len(scores)
        offsprings = [Individual(c, s[0], s[1]) for c, s in zip(offsprings, scores)]
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
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: HallOfFame | None = None,
    workers_num: int = 0,
):
    stats = Statistics()
    logger = log.getCoreLogger()

    # only use the physical cores
    pool = Pool(workers_num, logical=False)

    # generate the initial population
    population = toolbox.generate(population_size)
    logger.debug(f"generated individuals: {len(population)}")

    for g in tqdm(range(max_generations), ncols=80, ascii=True):
        selected = toolbox.select(population, population_size)
        logger.debug(f"selected individuals: {len(selected)}")

        couples = batch.mating(selected)
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
