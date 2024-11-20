import json
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
    # sequential simulation
    sequential.main(argv)
    lines = read_file("logs/sequential.json")
    stats = parse_values(lines)

    # parallel simulation
    parallel.main(argv)
    lines = read_file("logs/parallel.json")
    pstats = parse_values(lines)

    print(stats)
    print(pstats)


if __name__ == "__main__":
    main(sys.argv)
