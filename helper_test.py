import argparse
import random
import time

import numpy as np

from ppga import algorithms, base, log, parallel, tools


def evaluate(chromosome: np.ndarray):
    for _ in range(50000):
        random.random()
    return (int(chromosome.sum()),)


if __name__ == "__main__":
    # CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="info", help="set the logging level")
    parser.add_argument(
        "--len", type=int, default=10, help="set the length of the chromosome"
    )
    args = parser.parse_args()

    # set the core logging level
    log.setLevel(args.log.upper())
    logger = log.getUserLogger()
    logger.setLevel(args.log.upper())

    # initialize the toolbox
    toolbox = base.ToolBox()
    toolbox.set_weights((1.0,))
    toolbox.set_generation(tools.gen_repetition, values=(0, 1), length=args.len)
    toolbox.set_selection(tools.sel_tournament, tournsize=3)
    toolbox.set_crossover(tools.cx_one_point)
    toolbox.set_mutation(tools.mut_bitflip)
    toolbox.set_evaluation(evaluate)

    # run the genetic algorithm
    hof = base.HallOfFame(50)
    arguments = {
        "toolbox": toolbox,
        "population_size": 5000,
        "keep": 0.1,
        "cxpb": 0.7,
        "mutpb": 0.3,
        "max_generations": 100,
        "hall_of_fame": hof,
    }

    workers_num = parallel.opt_workers_num(
        algorithms.elitist, algorithms.pelitist, **arguments
    )

    # population, stats = algorithms.pelitist(
    #     toolbox=toolbox,
    #     population_size=100,
    #     keep=0.1,
    #     cxpb=0.7,
    #     mutpb=0.3,
    #     max_generations=100,
    #     hall_of_fame=hof,
    #     workers_num=workers_num,
    # )

    logger.info(f"best fitness: {hof[0].fitness}")
