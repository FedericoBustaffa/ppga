import numpy as np
from numpy import random


def cx_one_point(father, mother) -> tuple:
    cx_point = random.randint(1, len(father))

    offspring1 = np.append(father[:cx_point], mother[cx_point:])
    offspring2 = np.append(mother[:cx_point], father[cx_point:])

    return offspring1, offspring2


def cx_one_point_ordered(father, mother) -> tuple:
    cx_point = random.randint(1, len(father) - 1)

    offspring1 = father[:cx_point]
    offspring2 = father[cx_point:]

    tail1 = np.isin(mother, offspring1)
    tail2 = np.isin(mother, offspring2)

    offspring1 = np.append(offspring1, mother[tail2])
    offspring2 = np.append(offspring2, mother[tail1])

    return offspring1, offspring2


def cx_two_points(father, mother) -> tuple:
    cx_point1, cx_point2 = random.choice(
        [i + 1 for i in range(len(father) - 2)], size=2, replace=False
    )

    if cx_point1 > cx_point2:
        cx_point1, cx_point2 = cx_point2, cx_point1

    offspring1 = np.concat(
        (father[:cx_point1], mother[cx_point1:cx_point2], father[cx_point2:])
    )

    offspring2 = np.concat(
        (mother[:cx_point1], father[cx_point1:cx_point2], mother[cx_point2:])
    )

    return offspring1, offspring2


def cx_uniform(father, mother, indpb: float = 0.5) -> tuple:
    assert indpb >= 0.0 and indpb <= 1.0

    offspring1 = np.array(father)
    offspring2 = np.array(mother)
    for i in range(len(father)):
        if random.random() < indpb:
            offspring1[i] = mother[i]
            offspring2[i] = father[i]

    return offspring1, offspring2


if __name__ == "__main__":
    father = random.choice([i for i in range(10)], size=10, replace=False)
    mother = random.choice([i for i in range(10)], size=10, replace=False)

    print(father, mother)

    o1, o2 = cx_uniform(father, mother)
    print(o1, o2)
