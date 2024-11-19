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
        if "BENCHMARK" in line:
            data.append(json.loads(line))

    return data


def parse_values(lines: list[dict]):
    stats = dict()
    for line in lines:
        process = line["process_name"]
        key = line["field"].removesuffix(":")

        try:
            proc_stats = stats[process]
        except KeyError:
            stats.update({process: {}})
            proc_stats = stats[process]

        try:
            proc_stats[key].append(float(line["time"]))
        except KeyError:
            proc_stats.update({key: []})
            proc_stats[key].append(float(line["time"]))

    return stats


def simulate_seq(argv: list[str]):
    sequential.main(argv)

    lines = read_file()
    stats = parse_values(lines)["MainProcess"]

    return stats


def simulate_par(argv: list[str]):
    parallel.main(argv)

    lines = read_file()
    stats = parse_values(lines)

    return stats


def main(argv: list[str]):
    stats = simulate_seq(argv)
    pstats = simulate_par(argv)

    print("-" * 15, "SEQUENTIAL", "-" * 15)
    for key in stats.keys():
        print(f"total {key} time: {np.sum(stats[key])} s")
        print(f"mean {key} time: {np.mean(stats[key]) * 1000.0} ms")
        print("-" * 50)

    print("-" * 15, "PARALLEL", "-" * 15)
    for worker in pstats.keys():
        print("-" * 15, worker, "-" * 15)
        for key in pstats[worker].keys():
            print(f"total {key} time: {np.sum(pstats[worker][key])} s")
            print(f"mean {key} time: {np.mean(pstats[worker][key]) * 1000.0} ms")
            print("-" * 50)


if __name__ == "__main__":
    main(sys.argv)
