import time

import matplotlib.pyplot as plt
import numpy as np

from ppga import algorithms, base, log, tools


def evaluate(chromosome: np.ndarray):
    return (int(chromosome.sum()),)


if __name__ == "__main__":
    # set the level to debug for all the logs
    log.setLevel("INFO")

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
    start = time.perf_counter()
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
    end = time.perf_counter()

    for ind in hof:
        logger.info(ind)

    plt.figure(figsize=(16, 9))
    plt.title("Biodiversity trend")
    plt.xlabel("Generation")
    plt.ylabel("Biodiversity")
    plt.plot([i for i in range(len(stats.diversity))], stats.diversity, c="g")
    plt.grid()
    plt.show()

    plt.figure(figsize=(16, 9))
    plt.title("Fitness trend")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.plot(
        [i for i in range(len(stats.worst))], stats.worst, c="r", label="worst score"
    )
    plt.plot([i for i in range(len(stats.mean))], stats.mean, c="b", label="mean score")
    plt.plot([i for i in range(len(stats.best))], stats.best, c="g", label="best score")
    plt.grid()
    plt.legend()
    plt.show()

    plt.figure(figsize=(16, 9))
    plt.title("Time trend")
    plt.xlabel("Generation")
    plt.ylabel("Time")
    plt.plot([i for i in range(len(stats.times))], stats.times)
    plt.grid()
    plt.show()

    logger.info(f"Total time: {end - start} seconds")
    logger.info(f"Total time spent in parallel: {np.sum(stats.times)} seconds")
