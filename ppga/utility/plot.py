import matplotlib.pyplot as plt

from ppga.base.statistics import Statistics

figsize = (16, 10)
dpi = 200


def fitness_trend(stats: Statistics):
    generations = [g for g in range(len(stats.max))]

    plt.figure(figsize=figsize, dpi=dpi)
    plt.title("Fitness trend")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.plot(generations, stats.max, label="Best fitness", c="g")
    plt.plot(generations, stats.mean, label="Mean fitness", c="b")
    plt.plot(generations, stats.min, label="Worst fitness", c="r")

    plt.grid()
    plt.legend()
    plt.show()


def biodiversity_trend(stats: Statistics):
    generations = [g for g in range(len(stats.diversity))]

    plt.figure(figsize=figsize, dpi=dpi)
    plt.title("Biodiversity trend")
    plt.ylim(0.0, 1.0)
    plt.xlabel("Generation")
    plt.ylabel("Biodiversity percentage")
    plt.plot(generations, stats.diversity, label="Biodiversity", c="g")

    plt.grid()
    plt.legend()
    plt.show()


def timing(timings: dict[str, float]):
    plt.figure(figsize=figsize, dpi=dpi)
    plt.title("Timing")
    plt.pie(
        [v for v in timings.values()],
        labels=[k for k in timings.keys()],
        autopct="%1.1f%%",
    )
    plt.show()


def evals(evals: list[int]):
    plt.figure(figsize=figsize, dpi=dpi)
    plt.title("Evaluations")
    plt.xlabel("Generation")
    plt.ylabel("Evals")

    plt.hist(evals, bins=20, edgecolor="black", label="evals")

    plt.legend()
    plt.grid()
    plt.show()


def multievals(evals: list[list[int]]):
    plt.figure(figsize=figsize, dpi=dpi)
    plt.title("Evaluations per worker")
    plt.xlabel("Worker")
    plt.ylabel("Number of evaluations")
    plt.xticks(list(range(len(evals[0]))))

    evals_per_worker = [0 for _ in range(len(evals[0]))]
    for e in evals:
        for i, n in enumerate(e):
            evals_per_worker[i] += n

    plt.bar(list(range(len(evals_per_worker))), evals_per_worker, label="bar")

    plt.legend()
    plt.show()
