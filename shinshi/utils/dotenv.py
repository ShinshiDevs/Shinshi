import logging
import os
from typing import TypeVar

T: TypeVar = TypeVar("T")


def dotenv_get_value(key: str, default: T | None) -> str:
    return os.environ.get(
        key.upper(),
        default
    ).upper()


def dotenv_get_log_level(key: str) -> int:
    return logging.getLevelName(
        dotenv_get_value(key, "INFO").upper()
    )


def dotenv_get_boolean(key: str) -> bool:
    return dotenv_get_value(key, False) == "TRUE"
