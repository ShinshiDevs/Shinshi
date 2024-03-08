import asyncio
import logging
from pathlib import Path

from shinshi.asyncio import setup_event_policy, create_loop
from shinshi.dotenv import load_dotenv
from shinshi.environment import Environment
from shinshi.logging.formatters import ConsoleFormatter
from shinshi.utils.dotenv import dotenv_get_log_level, dotenv_get_boolean

setup_event_policy()
loop: asyncio.AbstractEventLoop = create_loop()
environment: Environment = Environment()

if load_dotenv(
    Path(environment.root_path, "secrets", "app.env")
) is None:
    raise RuntimeError("Unable to load dotenv file.")

stream_handler: logging.StreamHandler = logging.StreamHandler()
stream_handler.setFormatter(ConsoleFormatter("%(asctime)s %(name)-40s %(levelname)-20s %(message)s"))
logging.basicConfig(
    level=dotenv_get_log_level("SHINSHI_LOG_LEVEL"),
    handlers=[stream_handler]
)
if dotenv_get_boolean("SHINSHI_IS_HIKARI_NETWORK_TRACE_ENABLED") is True:
    rest_logger: logging.Logger = logging.getLogger("hikari.rest")
    rest_logger.setLevel("HIKARI_TRACE")

if __name__ == "__main__":
    loop.set_debug(dotenv_get_boolean("SHINSHI_ASYNCIO_DEBUG"))
    # After some working...
    # TODO: Kernel (just for services start, not more)
    # TODO: Bot Service (just for correct start and stop, with hikari trace enable)
    # TODO: DiscordBot and Cache classes
    # TODO: Command and component handler (T-T)
    #   This task includes many items, so... I need to write a roadmap somewhere.
    # TODO: Data provider and HTTP Pool (with orjson serializer)
    # TODO: With command handler - Workflows and Workflows Manager, Workflows Repository, and Event Manager.
    # TODO: Maybe little changes in .editorconfig and create one style for any file of Shinshi.
    # TODO: Finish this file and check is I18nProvider working or not??
    #   (because it was little bit change and I don't know)
