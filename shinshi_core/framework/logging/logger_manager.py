from typing import Sequence

from .enums import LogLevel
from .logger_wrapper import LoggerWrapper


class LoggerManager:
    __slots__: Sequence[str] = ()

    @staticmethod
    def set_min_log_level(min_log_level: LogLevel) -> None:
        LoggerWrapper.set_min_log_level(min_log_level)
