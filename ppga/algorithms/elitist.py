from ppga import tools
from ppga.algorithms.custom import custom, pcustom
from ppga.base import HallOfFame, ToolBox


def elitist(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
):
    toolbox.set_replacement(tools.elitist, keep=keep)

    return custom(
        toolbox,
        population_size,
        cxpb,
        mutpb,
        max_generations,
        hall_of_fame,
    )


def pelitist(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
):
    toolbox.set_replacement(tools.elitist, keep=keep)

    return pcustom(
        toolbox,
        population_size,
        cxpb,
        mutpb,
        max_generations,
        hall_of_fame,
    )
