import asyncio
from os import environ
from typing import Sequence

from hikari.impl import config
from hikari.intents import Intents

import shinshi
from shinshi.constants import resources_dir
from shinshi.data import DataProvider
from shinshi.discord.bot import Bot
from shinshi.events import StoppingEvent, StartingEvent, event_manager
from shinshi.http import HttpPoolClient
from shinshi.i18n import I18nProvider

__all__: Sequence[str] = ("http_pool_client", "i18n_provider", "data_provider")

http_pool_client: HttpPoolClient = HttpPoolClient()
i18n_provider: I18nProvider = I18nProvider(resources_dir / "i18n")
data_provider: DataProvider = DataProvider(resources_dir)

Bot(
    token=environ.get("SHINSHI_DISCORD_TOKEN"),
    data_provider=data_provider,
    banner_extras={
        "shinshi_copyright": shinshi.__copyright__,
        "shinshi_license": shinshi.__license__,
        "shinshi_discord_invite": shinshi.__support__,
        "shinshi_github_url": shinshi.__github__,
    },
    http_settings=config.HTTPSettings(enable_cleanup_closed=False),
    intents=Intents.GUILDS
            | Intents.GUILD_EMOJIS
            | Intents.GUILD_MESSAGES
            | Intents.GUILD_MODERATION
)


def run(loop: asyncio.AbstractEventLoop) -> None:
    try:
        loop.run_until_complete(event_manager.emit(StartingEvent))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(event_manager.emit(StoppingEvent))
