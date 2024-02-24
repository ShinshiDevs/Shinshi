import logging
from collections.abc import Callable
from typing import Any
from typing import Sequence

from shinshi_core.framework.logging import Logger
from shinshi_core.framework.logging.formatters import DefaultExternalLogFormatterInstance


def default_writer(instance: Logger, message: str) -> None:
    instance.trace(message)


_LOG_WRITERS: dict[int, Callable[[Logger, str], None]] = {
    logging.CRITICAL: lambda instance, message: instance.critical(message),
    logging.ERROR: lambda instance, message: instance.error(message),
    logging.WARNING: lambda instance, message: instance.warning(message),
    logging.INFO: lambda instance, message: instance.info(message),
    logging.DEBUG: lambda instance, message: instance.debug(message),
    logging.NOTSET: default_writer,
}


class ForwardEntryHandler(logging.Handler):
    __slots__: Sequence[str] = ("__target", "__formatter")

    def __init__(
        self, target: Logger, formatter: Any = DefaultExternalLogFormatterInstance
    ) -> None:
        super().__init__()
        self.__target = target
        self.__formatter = formatter

    def emit(self, record):
        if (writer := _LOG_WRITERS.get(record.levelno)) is None:
            writer = default_writer
        writer(self.__target, self.__formatter.format(record))
