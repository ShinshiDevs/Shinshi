from os import getenv

from aurum import SyncCommandsFlag
from dotenv import load_dotenv
from hikari.impl import CacheComponents, CacheSettings
from hikari.intents import Intents
from hikari.presences import Activity

from shinshi import events, extensions
from shinshi.bot import Bot
from shinshi.bot.client import Client
from shinshi.i18n import I18nProvider
from shinshi.utils.logging import setup_logging
from shinshi.utils.loop import install_uvloop
from shinshi.utils.version import get_version


def main() -> None:
    install_uvloop()
    setup_logging()
    load_dotenv()

    bot: Bot = Bot(
        getenv("SHINSHI_DISCORD_TOKEN"),
        intents=Intents.NONE | Intents.GUILDS | Intents.GUILD_EMOJIS,
        cache_settings=CacheSettings(
            components=CacheComponents.NONE
            | CacheComponents.ME
            | CacheComponents.GUILDS
            | CacheComponents.GUILD_CHANNELS
            | CacheComponents.GUILD_STICKERS
            | CacheComponents.MEMBERS
            | CacheComponents.ROLES
            | CacheComponents.EMOJIS,
            max_messages=1000,
            max_dm_channel_ids=0,
        ),
        banner=None,
    )
    client: Client = Client(
        bot=bot,
        l10n=I18nProvider("i18n"),
        sync_commands=SyncCommandsFlag.NONE,
    )

    client.load_events(events.__name__)
    client.extensions.load_extensions(extensions.__name__, extensions.__path__)
    client.add_starting_task(client.extensions.sync_commands())

    client.run(activity=Activity(name=f"v{get_version()}"))


if __name__ == "__main__":
    main()
