import logging
import sys

from colorama import Back, Fore

FMT = "[{levelname}] {name}: {message}"


DEBUG = logging.DEBUG
SUCCESS = 15
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

levels = {
    "DEBUG": DEBUG,
    "SUCCESS": SUCCESS,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}

logging.addLevelName(15, "SUCCESS")

FORMATS = {
    logging.DEBUG: Fore.CYAN + FMT + Fore.RESET,
    SUCCESS: Fore.GREEN + FMT + Fore.RESET,
    logging.INFO: Fore.RESET + FMT + Fore.RESET,
    logging.WARNING: Fore.YELLOW + FMT + Fore.RESET,
    logging.ERROR: Fore.RED + FMT + Fore.RESET,
    logging.CRITICAL: Back.RED + Fore.WHITE + FMT + Fore.RESET + Back.RESET,
}


class ColorFormatter(logging.Formatter):
    """Formatter the provides colors through colorama module"""

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(FORMATS[record.levelno], style="{")
        return formatter.format(record)


class Logger(logging.Logger):
    """Wrapper around the Logger class of the `logging` module"""

    def __init__(self, name, level):
        super().__init__(name, level)

    def success(self, message) -> None:
        super().log(SUCCESS, message)


core_logger = Logger("CORE", WARNING)
formatter = ColorFormatter()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(WARNING)
handler.setFormatter(formatter)
core_logger.addHandler(handler)


user_logger = Logger("USER", INFO)
formatter = ColorFormatter()
handler = logging.StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(formatter)
user_logger.addHandler(handler)


def getCoreLogger(level: str | int = WARNING) -> Logger:
    """Returns the core logger with the given level set on all handlers"""
    if isinstance(level, str):
        level = levels[level]
    setCoreLevel(level)

    return core_logger


def setCoreLevel(level: str | int) -> None:
    """Set the core logger log level"""
    for h in core_logger.handlers:
        h.setLevel(level)
    core_logger.setLevel(level)


def getLogger(level: str | int = INFO) -> Logger:
    """Provides a logger for the user with the given log level"""
    if isinstance(level, str):
        level = levels[level]

    user_logger.setLevel(level)
    for h in user_logger.handlers:
        h.setLevel(level)

    return user_logger
