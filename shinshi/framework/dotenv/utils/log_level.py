import logging
from os import environ


def get_log_level() -> int:
    return logging.getLevelName(environ.get("SHINSHI_LOG_LEVEL", "INFO").upper())
