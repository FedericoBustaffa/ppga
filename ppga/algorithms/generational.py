from ppga import tools
from ppga.algorithms.custom import custom, pcustom
from ppga.base import HallOfFame, ToolBox


def generational(
    toolbox: ToolBox,
    population_size: int,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
):
    toolbox.set_replacement(tools.total)

    return custom(
        toolbox=toolbox,
        population_size=population_size,
        keep=0.0,
        cxpb=cxpb,
        mutpb=mutpb,
        max_generations=max_generations,
        hall_of_fame=hall_of_fame,
    )


def pgenerational(
    toolbox: ToolBox,
    population_size: int,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
):
    toolbox.set_replacement(tools.total)

    return pcustom(
        toolbox=toolbox,
        population_size=population_size,
        keep=0.0,
        cxpb=cxpb,
        mutpb=mutpb,
        max_generations=max_generations,
        hall_of_fame=hall_of_fame,
    )
