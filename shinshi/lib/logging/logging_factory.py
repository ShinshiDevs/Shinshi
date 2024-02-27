from typing import Sequence

import structlog
from structlog import BoundLogger

from shinshi.lib.utils import get_full_name


class LoggerFactory:
    __slots__: Sequence[str] = ()

    @staticmethod
    def create(instance: type | str) -> BoundLogger:
        name = get_full_name(instance) if not isinstance(instance, str) else instance
        return structlog.get_logger(logger_name=name)
