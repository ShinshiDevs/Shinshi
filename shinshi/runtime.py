import asyncio
from concurrent.futures import ThreadPoolExecutor
from os import environ

from hikari.impl import config
from hikari.intents import Intents

from shinshi import __copyright__, __license__, __support__, __github__
from shinshi.bot import Bot
from shinshi.constants import resources_dir
from shinshi.data import DataProvider
from shinshi.events import StoppingEvent, StartingEvent, event_manager
from shinshi.http import HttpPoolClient
from shinshi.i18n import I18nProvider

http_pool_client: HttpPoolClient = HttpPoolClient()
i18n_provider: I18nProvider = I18nProvider(resources_dir / "i18n")
data_provider: DataProvider = DataProvider(resources_dir)
bot: Bot = Bot(
    token=environ.get("SHINSHI_DISCORD_TOKEN"),
    data_provider=data_provider,
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
            | Intents.GUILD_MODERATION
)


def run(loop: asyncio.AbstractEventLoop) -> None:
    try:
        loop.run_until_complete(event_manager.send(StartingEvent))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(event_manager.send(StoppingEvent))
