"""Entry point"""
from os import environ
from concurrent.futures import ThreadPoolExecutor

from shinshi_core.sdk.asyncio import setup_event_policy, setup_loop
from shinshi_core.sdk.dotenv import load_dotenv
from shinshi_core.sdk.environment import Environment
from shinshi_core.framework.logging.enums import LogLevel
from shinshi_core.framework.logging.utils import configure_logging


if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=15)
    _, loop = setup_event_policy(), setup_loop()
    loop.set_default_executor(executor)

    environment = Environment()

    if environ.get("SHINSHI_ENVIRONMENT") != "docker":
        if load_dotenv(f"{environment.root_path}/app.env") is False:
            raise RuntimeWarning(".env file doesn't loaded correctly")

    log_level = LogLevel.parse(environ.get("SHINSHI_LOG_LEVEL"))
    logger, logger_manager, logger_factory = configure_logging(log_level)
else:
    raise RuntimeError()
