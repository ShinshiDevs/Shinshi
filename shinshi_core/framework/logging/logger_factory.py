from typing import Sequence

from shinshi_core.sdk.utils import get_full_name
from .logger import Logger
from .logger_manager import LoggerManager


class LoggerFactory:
    __slots__: Sequence[str] = ("__logger_manager",)

    def __init__(self, logger_manager: LoggerManager) -> None:
        self.__logger_manager = logger_manager

    def create(self, target_type: type | str) -> Logger:
        return Logger(
            get_full_name(target_type)
            if isinstance(target_type, type)
            else target_type,
        )
