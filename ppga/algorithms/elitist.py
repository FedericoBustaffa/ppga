from ppga import log, tools
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
    log_level: str | int = log.WARNING,
):
    toolbox.set_replacement(tools.elitist, keep=keep)

    return custom(
        toolbox,
        population_size,
        keep,
        cxpb,
        mutpb,
        max_generations,
        hall_of_fame,
        log_level,
    )


def pelitist(
    toolbox: ToolBox,
    population_size: int,
    keep: float = 0.5,
    cxpb: float = 0.8,
    mutpb: float = 0.2,
    max_generations: int = 50,
    hall_of_fame: None | HallOfFame = None,
    log_level: str | int = log.WARNING,
):
    toolbox.set_replacement(tools.elitist, keep=keep)

    return pcustom(
        toolbox,
        population_size,
        keep,
        cxpb,
        mutpb,
        max_generations,
        hall_of_fame,
        log_level,
    )
