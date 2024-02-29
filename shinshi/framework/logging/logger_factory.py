import logging

from shinshi.sdk.utils import get_full_name


class LoggerFactory:
    @staticmethod
    def create(instance: type | str) -> logging.Logger:
        name: str = get_full_name(instance) if not isinstance(instance, str) else instance
        return logging.getLogger(name)
