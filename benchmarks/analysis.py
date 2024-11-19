import json
import sys

import numpy as np
import parallel
import sequential


def read_file() -> list[dict]:
    file = open("logs/log.json", "r")
    lines = file.readlines()
    file.close()

    data = []
    for line in lines:
        data.append(json.loads(line))

    return data


def parse_values(lines: list[str], times: dict[str, list]):
    for line in lines:
        words = line.split(" ")
        key = words[-3].removesuffix(":")
        times[key].append(float(line.split(" ")[-2]))

    return times


def simulate_seq(argv: list[str]):
    sequential.main(argv)

    times = {
        "generation": [],
        "selection": [],
        "crossover": [],
        "mutation": [],
        "evaluation": [],
        "replacement": [],
        "stime": [],
    }

    data = read_file()
    times = parse_values(data, times)

    for key in times.keys():
        print(f"total {key} time: {np.sum(times[key])} s")
        print(f"mean {key} time: {np.mean(times[key]) * 1000.0} ms")
        print("-" * 50)

    return times


def parse_values_p(lines: list, times: dict[str, list]):
    workers = []

    for line in lines:
        words = line.split(" ")
        key = words[-3].removesuffix(":")
        try:
            times[key].append(float(line.split(" ")[-2]))
        except KeyError:
            pass

    return times


def simulate_par(argv: list[str]):
    parallel.main(argv)

    times = {
        "generation": [],
        "selection": [],
        "crossover": [],
        "mutation": [],
        "evaluation": [],
        "replacement": [],
        "parallel": [],
        "ptime": [],
    }

    lines = read_file()
    times = parse_values_p(lines, times)

    return times


def main(argv: list[str]):
    stimes = simulate_seq(argv)
    # ptimes = simulate_par(argv)


if __name__ == "__main__":
    main(sys.argv)
)
