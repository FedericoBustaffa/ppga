import sys

import numpy as np


def read_file() -> list[str]:
    file = open("logs/benchmark.log", "r")
    lines = file.readlines()
    lines.sort(key=lambda x: x.split(" ")[-3])
    file.close()

    return lines


def sequential_analysis():
    times = {
        "generation": [],
        "selection": [],
        "crossover": [],
        "mutation": [],
        "evaluation": [],
        "replacement": [],
        "stime": [],
    }

    lines = read_file()
    for line in lines:
        words = line.split(" ")
        key = words[-3].removesuffix(":")
        times[key].append(float(line.split(" ")[-2]))

    for key in times.keys():
        print(f"total {key} time: {np.sum(times[key])} s")
        print(f"mean {key} time: {np.mean(times[key]) * 1000.0} ms")
        print("-" * 50)


def parallel_analysis():
    times = {
        "generation": [],
        "selection": [],
        "crossover": [],
        "mutation": [],
        "evaluation": [],
        "replacement": [],
        "ptime": [],
        "parallel": [],
    }

    lines = read_file()
    for line in lines:
        words = line.split(" ")
        key = words[-3].removesuffix(":")
        times[key].append(float(line.split(" ")[-2]))

    for key in times.keys():
        print(f"total {key} time: {np.sum(times[key])} s")
        print(f"mean {key} time: {np.mean(times[key]) * 1000.0} ms")
        print("-" * 50)


def main(argv: list[str]):
    sequential_analysis()
    # parallel_analysis()


if __name__ == "__main__":
    main(sys.argv)
