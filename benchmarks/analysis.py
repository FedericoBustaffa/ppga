import json
import os
import sys

import pandas as pd
import parallel
import sequential


def read_file(filepath: str) -> list[dict]:
    file = open(filepath, "r")
    lines = file.readlines()
    file.close()

    data = []
    for line in lines:
        if "BENCHMARK" in line:
            data.append(json.loads(line))

    return data


def parse_values(lines: list[dict]) -> pd.DataFrame:
    stats = {"process_name": [], "field": [], "time": []}
    for line in lines:
        stats["process_name"].append(line["process_name"])
        stats["field"].append(line["field"])
        stats["time"].append(line["time"])

    return pd.DataFrame(stats)


def main(argv: list[str]):
    # backups results dir
    if "results" not in os.listdir("."):
        os.mkdir("results")

    # sequential simulation
    sequential.main(argv)
    lines = read_file("logs/sequential.json")
    stats = parse_values(lines)
    stats.to_csv("results/sequential.csv", header=True, index=False)

    # parallel simulation
    parallel.main(argv)
    lines = read_file("logs/parallel.json")
    pstats = parse_values(lines)
    pstats.to_csv("results/parallel.csv", header=True, index=False)

    stime = stats[stats["field"] == "stime"]["time"].sum()
    ptime = pstats[pstats["field"] == "ptime"]["time"].sum()

    print(f"sequential time: {stime} seconds")
    print(f"parallel time: {ptime} seconds")
    print(f"speed up: {stime / ptime}")


if __name__ == "__main__":
    main(sys.argv)
