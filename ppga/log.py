import datetime as dt
import json
import logging
import logging.handlers
import os
import sys

from colorama import Back, Fore

# variable for setting up only one time
setted = False

FILE = "%(filename)s:%(lineno)d"
FMT = "[%(levelname)s]: %(message)s"

logging.addLevelName(15, "BENCHMARK")

FORMATS = {
    logging.DEBUG: Fore.CYAN + FMT + Fore.RESET,
    logging.INFO: Fore.RESET + FMT + Fore.RESET,
    15: Fore.GREEN + FMT + Fore.RESET,
    logging.WARNING: Fore.YELLOW + FMT + Fore.RESET,
    logging.ERROR: Fore.RED + FMT + Fore.RESET,
    logging.CRITICAL: Back.RED + Fore.RESET + FMT + Fore.RESET + Back.RESET,
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(
            fmt="%(asctime)s | "
            + Fore.CYAN
            + FILE
            + Fore.RESET
            + " | %(name)s %(processName)s "
            + FORMATS[record.levelno],
            datefmt=Fore.GREEN + "%d-%m-%Y - %H:%M:%S" + Fore.RESET,
        )
        return formatter.format(record)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if record.levelname == "BENCHMARK":
            message = record.getMessage()
            words = message.split(" ")
            field = words[-3]
            elapsed_time = words[-2]

            records = {
                "timestamp": dt.datetime.fromtimestamp(
                    record.created, tz=dt.timezone.utc
                ).isoformat(),
                "logger": record.name,
                "process_name": record.processName,
                "level": record.levelname,
                "field": field.removesuffix(":"),
                "time": float(elapsed_time),
            }
        else:
            records = {
                "timestamp": dt.datetime.fromtimestamp(
                    record.created, tz=dt.timezone.utc
                ).isoformat(),
                "logger": record.name,
                "process_name": record.processName,
                "level": record.levelname,
                "message": record.getMessage(),
            }

        return json.dumps(records, default=str)


def setup():
    global setted
    setted = True

    # formatters
    color_formatter = ColorFormatter()
    json_formatter = logging.Formatter(
        fmt="%(asctime)s | %(filename)s:%(lineno)d | %(name)s %(processName)s | [%(levelname)s]: %(message)s",
        datefmt="%d-%m-%Y - %H:%M:%S",
    )

    if "logs" not in os.listdir():
        os.mkdir("logs")

    file_handler = logging.FileHandler(filename="logs/log.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(json_formatter)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(color_formatter)

    core_logger = logging.getLogger("CORE")
    core_logger.setLevel(logging.WARNING)
    core_logger.addHandler(file_handler)
    core_logger.addHandler(stdout_handler)

    user_logger = logging.getLogger("USER")
    user_logger.setLevel(logging.INFO)
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
