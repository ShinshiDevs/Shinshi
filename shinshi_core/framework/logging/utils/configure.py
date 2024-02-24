import logging

import structlog

from shinshi_core.framework.logging import Logger
from shinshi_core.framework.logging import LoggerFactory
from shinshi_core.framework.logging import LoggerManager
from shinshi_core.framework.logging import LoggerWrapper
from shinshi_core.framework.logging.enums import LogLevel
from shinshi_core.framework.logging.handlers import ForwardEntryHandler


def configure_logging(
    log_level: LogLevel,
) -> tuple[Logger, LoggerManager, LoggerFactory]:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper("%Y-%m-%d %H:%M:%S"),
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=LoggerWrapper,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logger = structlog.get_logger(logger_name=__package__)
    logger_manager = LoggerManager()
    logger_manager.set_min_log_level(log_level)
    logger_factory = LoggerFactory(logger_manager)
    logging.basicConfig(level=logging.INFO, handlers=[ForwardEntryHandler(logger)])
    logger.info("configured logging", log_level=log_level.name or log_level.value)
    return logger, logger_manager, logger_factory
