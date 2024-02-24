from collections.abc import Callable
from typing import Any
from typing import Sequence

import structlog

from shinshi_core.sdk.utils import format_exception


class Logger:
    __slots__: Sequence[str] = ("__logger", "__get_min_log_level")

    def __init__(self, name: str) -> None:
        self.__logger = structlog.get_logger(logger_name=name)

    def trace(self, message: str, exception: Exception | None = None, **kwargs) -> None:
        Logger.__log(message, exception, kwargs, self.__logger.debug)

    def debug(self, message: str, exception: Exception | None = None, **kwargs) -> None:
        Logger.__log(message, exception, kwargs, self.__logger.debug)

    def info(self, message: str, exception: Exception | None = None, **kwargs) -> None:
        Logger.__log(message, exception, kwargs, self.__logger.info)

    def warning(self, message: str, exception: Exception | None = None, **kwargs) -> None:
        Logger.__log(message, exception, kwargs, self.__logger.warning)

    def error(self, message: str, exception: Exception | None = None, **kwargs) -> None:
        Logger.__log(message, exception, kwargs, self.__logger.error)

    def critical(self, message: str, exception: Exception | None = None, **kwargs) -> None:
        Logger.__log(message, exception, kwargs, self.__logger.critical)

    def exception(self, message: str, **kwargs) -> None:
        self.__logger.exception(message, **kwargs)

    @staticmethod
    def __log(
        message: str,
        exception: Exception | None,
        arguments: dict[str, Any],
        method: Callable[..., None],
    ) -> None:
        method(
            message,
            exception=format_exception(exception) if exception else None,
            exception_message=str(exception),
            **arguments,
        )
