import asyncio

from hikari.presences import Activity
from hikari.impl import CacheComponents
from hikari.intents import Intents

from shinshi import __version__, extensions
from shinshi.abc.bot.ibot_service import IBotService
from shinshi.abc.config.iconfiguration_service import IConfigurationService
from shinshi.abc.database.idatabase_service import IDatabaseService
from shinshi.abc.extensions.iextensions_service import IExtensionsService
from shinshi.abc.http.ihttp_service import IHTTPService
from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.framework.bot.bot_service import BotService
from shinshi.framework.config.configuration_service import ConfigurationService
from shinshi.framework.database.database_service import DatabaseService
from shinshi.framework.extensions.extensions_service import ExtensionsService
from shinshi.framework.http.http_service import HTTPService
from shinshi.framework.i18n.i18n_provider import I18nProvider
from shinshi.framework.kernel import Kernel
from shinshi.utils.loop import get_event_loop_policy


async def main() -> None:
    kernel: Kernel = Kernel()
    configuration_service: IConfigurationService = ConfigurationService(
        configs=["resources/emojis.yaml"]
    )
    configuration_service.setup_logging()
    configuration_service.load_dotenv()

    kernel.register_service(IConfigurationService, configuration_service)
    kernel.register_service(IHTTPService, HTTPService())
    kernel.register_service(II18nProvider, I18nProvider("resources/i18n"))
    kernel.register_service(IDatabaseService, DatabaseService())
    kernel.register_service(
        IBotService,
        BotService(
            i18n_provider=kernel.get_service(II18nProvider),
            cache_components=CacheComponents.ME
            | CacheComponents.GUILDS
            | CacheComponents.GUILD_CHANNELS
            | CacheComponents.GUILD_STICKERS
            | CacheComponents.MEMBERS
            | CacheComponents.ROLES
            | CacheComponents.EMOJIS,
            intents=Intents.GUILDS | Intents.GUILD_EMOJIS,
            activity=Activity(name=f"{__version__.version}"),
        ),
    )
    kernel.register_service(
        IExtensionsService,
        ExtensionsService(
            bot_service=kernel.get_service(IBotService),
            extensions_package=extensions.__name__,
            extensions_path=extensions.__path__,
        ),
    )
    await kernel.run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(get_event_loop_policy())
    asyncio.run(main())
