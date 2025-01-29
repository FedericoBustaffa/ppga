import random

import numpy as np


def cx_one_point(father, mother) -> tuple:
    cx_point = random.randint(1, len(father) - 1)

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
    cx_point1, cx_point2 = random.sample([i for i in range(1, len(father) - 1, 1)], k=2)
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


def cx_blend(father, mother, alpha: float = 0.5) -> tuple:
    g_min = np.minimum(father, mother)
    g_max = np.maximum(father, mother)
    interval = g_max - g_min

    lower_bound = g_min - alpha * interval
    upper_bound = g_max + alpha * interval

    offspring1 = np.random.uniform(lower_bound, upper_bound)
    offspring2 = np.random.uniform(lower_bound, upper_bound)

    return offspring1, offspring2
