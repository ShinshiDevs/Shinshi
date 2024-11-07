import asyncio

from hikari import Activity
from hikari.impl import CacheComponents
from hikari.intents import Intents

from shinshi import __version__, extensions
from shinshi.framework.bot.bot_service import BotService
from shinshi.framework.config.configuration_service import ConfigurationService
from shinshi.framework.database.database_service import DatabaseService
from shinshi.framework.extensions.extensions_service import ExtensionsService
from shinshi.framework.http.http_service import HTTPService
from shinshi.framework.i18n.i18n_provider import I18nProvider
from shinshi.framework.kernel import Kernel
from shinshi.utils.loop import get_event_loop_policy


async def main() -> None:
    configuration_service: ConfigurationService = ConfigurationService()
    configuration_service.configure_logging()
    configuration_service.load_dotenv()

    http_service: HTTPService = HTTPService()
    i18n_provider: I18nProvider = I18nProvider("resources/i18n")
    database_service: DatabaseService = DatabaseService("shinshi.abc.database.models")
    bot_service: BotService = BotService(
        i18n_provider=i18n_provider,
        cache_components=CacheComponents.ME
        | CacheComponents.GUILDS
        | CacheComponents.GUILD_CHANNELS
        | CacheComponents.GUILD_STICKERS
        | CacheComponents.MEMBERS
        | CacheComponents.ROLES
        | CacheComponents.EMOJIS,
        intents=Intents.GUILDS | Intents.GUILD_EMOJIS,
        activity=Activity(name=f"{__version__.version}")
    )
    extensions_service: ExtensionsService = ExtensionsService(
        bot_service, extensions.__name__, extensions.__path__
    )

    await Kernel(
        configuration_service,
        http_service,
        i18n_provider,
        database_service,
        bot_service,
        extensions_service,
    ).run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(get_event_loop_policy())
    asyncio.run(main())
