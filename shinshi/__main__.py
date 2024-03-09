import asyncio
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from os import environ
from pathlib import Path

import orjson
from hikari.impl import HTTPSettings
from hikari.intents import Intents

from shinshi.aiohttp.http_pool import HttpPool
from shinshi.asyncio import setup_event_policy, create_loop
from shinshi.bot import BotService, DiscordBot
from shinshi.dotenv import load_dotenv
from shinshi.environment import Environment
from shinshi.kernel import Kernel
from shinshi.logging.formatters import ConsoleFormatter
from shinshi.providers.data.data_provider import DataProvider
from shinshi.providers.i18n import I18nProvider
from shinshi.utils.dotenv import dotenv_get_log_level, dotenv_get_boolean

# TODO: Command and component handler (T-T)
#   This task includes many items, so... I need to write a roadmap somewhere.
# TODO: With command handler - Workflows and Workflows Manager, Workflows Repository.
# TODO: Maybe little changes in .editorconfig and create one style for any file of Shinshi.
# TODO: Finish this file and check is I18nProvider working or not??
#   (because it was little bit change and I don't know)

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

http_pool: HttpPool = HttpPool(loop)
i18n_provider: I18nProvider = I18nProvider(Path(environment.root_path, "resources", "i18n"))
data_provider: DataProvider = DataProvider(Path(environment.root_path, "resources"))
bot: DiscordBot = DiscordBot(
    data_provider,
    token=environ.get("SHINSHI_DISCORD_TOKEN"),
    executor=ThreadPoolExecutor(),
    intents=Intents.GUILDS
            | Intents.GUILD_EMOJIS
            | Intents.GUILD_MESSAGES
            | Intents.GUILD_MODERATION,
    logs=dotenv_get_log_level("SHINSHI_LOG_LEVEL"),
    loads=orjson.loads,
    dumps=orjson.dumps,
    http_settings=HTTPSettings(enable_cleanup_closed=False),
)
bot_service: BotService = BotService(loop, bot)

if __name__ == "__main__":
    loop.set_debug(dotenv_get_boolean("SHINSHI_ASYNCIO_DEBUG"))
    kernel: Kernel = Kernel(
        loop,
        (
            http_pool,
            i18n_provider,
            data_provider,
            bot_service
        )
    )
    try:
        kernel.run()
    except KeyboardInterrupt:
        sys.exit(0)
else:
    sys.exit(0)
