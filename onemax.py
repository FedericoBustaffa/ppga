import numpy as np

from ppga import algorithms, base, log, tools


def evaluate(chromosome: np.ndarray):
    return (int(chromosome.sum()),)


if __name__ == "__main__":
    # set the level to debug for all the logs
    log.setLevel("DEBUG")

    # different logger
    logger = log.getUserLogger()
    logger.setLevel("INFO")

    toolbox = base.ToolBox()

    # maximization problem
    toolbox.set_weights((1.0,))

    # generates a chromosome of 0 and 1 of length 10
    toolbox.set_generation(tools.gen_repetition, (0, 1), 10)
    toolbox.set_selection(tools.sel_tournament, tournsize=2)
    toolbox.set_crossover(tools.cx_one_point)
    toolbox.set_mutation(tools.mut_bitflip, indpb=0.5)
    toolbox.set_evaluation(evaluate)

    hof = base.HallOfFame(10)
    population, stats = algorithms.simple(
        toolbox=toolbox,
        population_size=100,
        keep=0.2,
        cxpb=0.7,
        mutpb=0.3,
        max_generations=100,
        hall_of_fame=hof,
        workers_num=-1,
    )

    for ind in hof:
        logger.info(ind)
