import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from os import environ
from typing import Tuple

from hikari.impl import config
from hikari.intents import Intents

from shinshi import __copyright__, __license__, __support__, __github__
from shinshi.bot import Bot
from shinshi.constants import logging_dir, dotenv_file, resources_dir
from shinshi.data import DataProvider
from shinshi.dotenv import load_dotenv
from shinshi.http import HttpPoolClient
from shinshi.i18n import I18nProvider
from shinshi.logging.utils import setup_logging

setup_logging(logging_dir / "configuration.yaml")
load_dotenv(dotenv_file) if environ.get("SHINSHI_ENVIRONMENT", "SYSTEM").upper != "DOCKER" else None

http_pool_client: HttpPoolClient = HttpPoolClient()
i18n_provider: I18nProvider = I18nProvider(resources_dir / "i18n")
data_provider: DataProvider = DataProvider(resources_dir)
bot: Bot = Bot(
    token=environ.get("SHINSHI_DISCORD_TOKEN"),
    banner_extras={
        "shinshi_copyright": __copyright__,
        "shinshi_license": __license__,
        "shinshi_discord_invite": __support__,
        "shinshi_github_url": __github__,
    },
    executor=ThreadPoolExecutor(),
    http_settings=config.HTTPSettings(enable_cleanup_closed=False),
    intents=Intents.GUILDS
            | Intents.GUILD_EMOJIS
            | Intents.GUILD_MESSAGES
            | Intents.GUILD_MODERATION,
    data_provider=data_provider,
)


def run(loop: asyncio.AbstractEventLoop) -> None:
    logger: logging.Logger = logging.getLogger("shinshi.runtime")
    services: Tuple[HttpPoolClient, I18nProvider, DataProvider] = (http_pool_client, i18n_provider, data_provider)
    try:
        logger.debug("starting services")
        for service in services:
            loop.run_until_complete(service.start())
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug("stopping")
        for service in services:
            if "stop" in service.__dir__():
                loop.run_until_complete(service.stop())
        loop.run_until_complete(bot.close())
        loop.stop()
