import random


def gen_repetition(values, length: int):
    return random.choices(values, k=length)


def gen_permutation(values):
    return random.sample(values, k=len(values))


if __name__ == "__main__":
    chromosome = gen_repetition([0, 1], 10)
    print(chromosome)

    chromosome = gen_permutation([i for i in range(10)])
    print(chromosome)
