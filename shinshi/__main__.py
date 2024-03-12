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
from shinshi.asyncio import create_loop
from shinshi.discord.bot import BotService, DiscordBot
from shinshi.dotenv import load_dotenv
from shinshi.environment import Environment
from shinshi.kernel import Kernel
from shinshi.logging.formatters import ConsoleFormatter
from shinshi.providers.data import DataProvider
from shinshi.providers.i18n import I18nProvider
from shinshi.utils.dotenv import dotenv_get_log_level, dotenv_get_boolean, dotenv_get_value

loop: asyncio.AbstractEventLoop = create_loop()
environment: Environment = Environment()
http_pool: HttpPool = HttpPool(loop)
if (resources_path := Path(environment.root_path, "resources")).exists():
    i18n_provider: I18nProvider = I18nProvider(resources_path / "i18n")
    data_provider: DataProvider = DataProvider(resources_path)
else:
    raise RuntimeError("No resources folder or not detected.")
if dotenv_get_value("SHINSHI_ENVIRONMENT") != "DOCKER":
    if load_dotenv(Path(environment.root_path, "secrets", "app.env")) is None:
        raise RuntimeError("Unable to load dotenv file.")

bot_service: BotService = BotService(
    loop,
    DiscordBot(
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
)
kernel: Kernel = Kernel(loop, (http_pool, i18n_provider, data_provider, bot_service))

if __name__ == "__main__":
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setFormatter(ConsoleFormatter("%(asctime)s %(name)-40s %(levelname)-20s %(message)s"))
    logging.basicConfig(level=dotenv_get_log_level("SHINSHI_LOG_LEVEL"), handlers=[stream_handler])
    loop.set_debug(dotenv_get_boolean("SHINSHI_ASYNCIO_DEBUG"))
    try:
        kernel.run()
    except KeyboardInterrupt:
        sys.exit(0)
else:
    sys.exit(0)
