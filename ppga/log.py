import logging
import logging.handlers
import sys

from colorama import Back, Fore

# variable for setting up only one time
setted = False

TIME = "%(asctime)s"
FILE = "%(filename)s:%(lineno)d"
FMT = "[%(levelname)s]: %(message)s"

logging.addLevelName(25, "BENCHMARK")

FORMATS = {
    logging.DEBUG: Fore.CYAN + FMT + Fore.RESET,
    logging.INFO: Fore.RESET + FMT + Fore.RESET,
    25: Fore.GREEN + FMT + Fore.RESET,
    logging.WARNING: Fore.YELLOW + FMT + Fore.RESET,
    logging.ERROR: Fore.RED + FMT + Fore.RESET,
    logging.CRITICAL: Back.RED + Fore.RESET + FMT + Fore.RESET + Back.RESET,
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(
            fmt=TIME
            + " | "
            + Fore.CYAN
            + FILE
            + Fore.RESET
            + " | %(name)s "
            + FORMATS[record.levelno],
            datefmt=Fore.GREEN + "%d-%m-%Y - %H:%M:%S" + Fore.RESET,
        )
        return formatter.format(record)


def setup():
    global setted
    setted = True
    formatter = logging.Formatter(
        fmt=TIME + " | " + FILE + " | %(name)s " + FMT,
        datefmt="%d-%m-%Y - %H:%M:%S",
    )

    color_formatter = ColorFormatter()

    file_handler = logging.FileHandler("logs/log.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    benchmark_handler = logging.FileHandler("logs/benchmark.log", mode="w")
    benchmark_handler.setLevel("BENCHMARK")
    benchmark_handler.setFormatter(formatter)
    benchmark_handler.addFilter(lambda record: record.levelname == "BENCHMARK")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(color_formatter)

    core_logger = logging.getLogger("CORE")
    core_logger.setLevel(logging.DEBUG)
    core_logger.addHandler(file_handler)
    core_logger.addHandler(benchmark_handler)
    core_logger.addHandler(stdout_handler)

    user_logger = logging.getLogger("USER")
    user_logger.setLevel(logging.DEBUG)
    user_logger.addHandler(file_handler)
    user_logger.addHandler(benchmark_handler)
    user_logger.addHandler(stdout_handler)


def setLevel(level: str | int):
    logger = logging.getLogger("CORE")
    logger.setLevel(level)


def getCoreLogger() -> logging.Logger:
    """Returns the core logger with the given level set on all handlers"""
    return logging.getLogger("CORE")


def getUserLogger() -> logging.Logger:
    """Provides a logger for the user with the given log level"""
    return logging.getLogger("USER")


if not setted:
    setup()
