import asyncio
from os import environ

import orjson
from hikari import Activity

import shinshi
from shinshi.constants import RESOURCES_DIR
from shinshi.data import DataProvider
from shinshi.discord.bot import Bot
from shinshi.events import event_manager
from shinshi.events.lifetime_events import StartingEvent, StoppingEvent
from shinshi.http import HttpPoolClient
from shinshi.i18n import I18nProvider

http_pool_client: HttpPoolClient = HttpPoolClient()
i18n_provider: I18nProvider = I18nProvider(RESOURCES_DIR / "i18n")
data_provider: DataProvider = DataProvider(RESOURCES_DIR)

bot: Bot = Bot(
    data_provider=data_provider,
    token=environ.get("SHINSHI_DISCORD_TOKEN"),
    banner=None,
    loads=orjson.loads,
    dumps=orjson.dumps,
)


def run(loop: asyncio.AbstractEventLoop) -> None:
    bot.print_banner(
        shinshi.__name__,
        True,
        False,
        {
            "shinshi_copyright": shinshi.__copyright__,
            "shinshi_license": shinshi.__license__,
            "shinshi_discord_invite": shinshi.__support__,
            "shinshi_github_url": shinshi.__github__,
        }
    )
    try:
        loop.run_until_complete(event_manager.emit(StartingEvent))
        loop.run_until_complete(
            bot.start(activity=Activity(name="Alterstein"))
        )
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(event_manager.emit(StoppingEvent))
        loop.run_until_complete(bot.close())
    finally:
        loop.close()
