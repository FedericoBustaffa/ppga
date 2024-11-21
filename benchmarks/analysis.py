import json
import os

import pandas as pd


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


def main():
    # backups results dir
    if "results" not in os.listdir("."):
        os.mkdir("results")

    # sequential simulation
    lines = read_file("logs/sequential.json")
    stats = parse_values(lines)
    stats.to_csv("results/sequential.csv", header=True, index=False)

    # parallel simulation
    lines = read_file("logs/parallel.json")
    pstats = parse_values(lines)
    pstats.to_csv("results/parallel.csv", header=True, index=False)

    stime = stats[stats["field"] == "stime"]["time"].sum()
    ptime = pstats[pstats["field"] == "ptime"]["time"].sum()

    # total time
    print(f"sequential time: {stime} seconds")
    print(f"parallel time: {ptime} seconds")
    print(f"speed up: {stime / ptime}")

    # take only the parallelized part
    cx_time = stats[stats["field"] == "crossover"]["time"].sum()
    mut_time = stats[stats["field"] == "mutation"]["time"].sum()
    eval_time = stats[stats["field"] == "evaluation"]["time"].sum()
    print(f"sequential cx + mut + eval time: {cx_time + mut_time + eval_time} seconds")

    # sync + work time
    parallel_time = pstats[pstats["field"] == "parallel"]["time"].sum()
    print(f"in parallel time: {parallel_time} seconds")

    # extract the worst worker time
    df = (
        pstats[pstats["process_name"] != "MainProcess"]
        .groupby(["process_name", "field"])
        .sum()
        .groupby("process_name")
        .sum()
    )

    worst_worker = df["time"].max()
    best_worker = df["time"].min()

    print(f"worst worker: {worst_worker} seconds")
    print(f"best worker: {best_worker} seconds")

    # approximate sync time
    print(f"sync time: {parallel_time - worst_worker} seconds")

    # pure speed up
    cx_mut_eval = cx_time + mut_time + eval_time
    print(f"pure speed up: {cx_mut_eval / parallel_time}")

    # mean evaluation time
    eval_st = stats[stats["field"] == "evaluation"]["time"].mean()
    print(f"mean eval stime: {eval_st} seconds")

    eval_pt = pstats[pstats["field"] == "evaluation"]["time"].mean()
    print(f"mean eval ptime: {eval_pt} seconds")

    eval_pt_per_worker = (
        pstats[pstats["field"] == "evaluation"]
        .groupby(["process_name", "field"])
        .mean()["time"]
    )
    print(f"min mean worker eval time: {eval_pt_per_worker.min()}")
    print(f"max mean worker eval time: {eval_pt_per_worker.max()}")


if __name__ == "__main__":
    main()
