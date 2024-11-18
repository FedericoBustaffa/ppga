import numpy as np


def main():
    file = open("logs/benchmark.log", "r")
    lines = file.readlines()
    file.close()

    lines.sort(key=lambda x: x.split(" ")[-3])
    times = {
        "generation": [],
        "selection": [],
        "crossover": [],
        "mutation": [],
        "evaluation": [],
        "replacement": [],
        "stime": [],
        "parallel": [],
    }

    for line in lines:
        words = line.split(" ")
        key = words[-3].removesuffix(":")
        times[key].append(float(line.split(" ")[-2]))

    for key in times.keys():
        print(f"total {key} time: {np.sum(times[key])} s")
        print(f"mean {key} time: {np.mean(times[key]) * 1000.0} ms")
        print("-" * 50)


if __name__ == "__main__":
    main()
