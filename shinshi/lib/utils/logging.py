import logging

import structlog
from structlog import BoundLogger

from shinshi.lib.logging import LoggerFactory


def configure_logging(log_level: int) -> (BoundLogger, LoggerFactory):
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper("%Y.%m.%d-%H:%M:%S"),
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True
    )
    logging.basicConfig(level=log_level)
    return structlog.get_logger(logger_name="shinshi"), LoggerFactory()
