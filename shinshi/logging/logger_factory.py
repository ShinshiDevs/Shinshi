import logging
from typing import Sequence

from shinshi.utils.class_name import get_class_name


class LoggerFactory:
    __slots__: Sequence[str] = ()

    @staticmethod
    def create(instance: type | str) -> logging.Logger:
        return logging.getLogger(
            get_class_name(instance) if not isinstance(instance, str) else instance
        )
