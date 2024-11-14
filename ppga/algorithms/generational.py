from ppga import log, tools
from ppga.algorithms.custom import custom, pcustom
from ppga.base import HallOfFame, ToolBox


def generational(
    toolbox: ToolBox,
    population_size: int,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
    log_level: str | int = log.WARNING,
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
        log_level=log_level,
    )


def pgenerational(
    toolbox: ToolBox,
    population_size: int,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
    log_level: str | int = log.WARNING,
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
        log_level=log_level,
    )
