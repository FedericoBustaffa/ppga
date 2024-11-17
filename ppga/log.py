import json
import logging
import logging.config

from colorama import Back, Fore

config_file = open("ppga/logger_config.json", "r")
configuration = json.load(config_file)
logging.config.dictConfig(configuration)
config_file.close()


def getCoreLogger() -> logging.Logger:
    """Returns the core logger with the given level set on all handlers"""
    return logging.getLogger("CORE")


def getUserLogger() -> logging.Logger:
    """Provides a logger for the user with the given log level"""
    return logging.getLogger("USER")
