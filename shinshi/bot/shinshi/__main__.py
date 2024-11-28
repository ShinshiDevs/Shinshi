import asyncio
import sys
from logging import Logger, getLogger
from pathlib import Path

from hikari.presences import Activity
from hikari.impl import CacheComponents
from hikari.intents import Intents

from shinshi import __version_info__, extensions
from shinshi.abc.bot.ibot_service import IBotService
from shinshi.abc.config.iconfiguration_service import IConfigurationService
from shinshi.abc.database.idatabase_service import IDatabaseService
from shinshi.abc.extensions.iextensions_manager import IExtensionsManager
from shinshi.abc.http.ihttp_service import IHTTPService
from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.framework.bot.bot_service import BotService
from shinshi.framework.config.configuration_service import ConfigurationService
from shinshi.framework.database.database_service import DatabaseService
from shinshi.framework.extensions.extensions_manager import ExtensionsManager
from shinshi.framework.http.http_service import HTTPService
from shinshi.framework.i18n.i18n_provider import I18nProvider
from shinshi.framework.kernel import Kernel
from shinshi.utils.loop import get_event_loop_policy


async def main() -> None:
    kernel: Kernel = Kernel()
    configuration_service: IConfigurationService = ConfigurationService(configs=[Path("resources/emojis.yaml")])
    configuration_service.setup_logging()
    configuration_service.load_dotenv()

    kernel.register_service(IConfigurationService, configuration_service)
    kernel.register_service(IHTTPService, HTTPService())
    kernel.register_service(II18nProvider, I18nProvider(Path("resources/i18n")))
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
            activity=Activity(name=f"{__version_info__.version}"),
        ),
    )
    kernel.register_service(
        IExtensionsManager,
        ExtensionsManager(kernel.get_service(IBotService), kernel.get_service(II18nProvider), module=extensions),
    )
    await kernel.run()


if __name__ == "__main__":
    logger: Logger = getLogger("shinshi.main")

    event_loop_policy: asyncio.AbstractEventLoopPolicy = get_event_loop_policy()
    asyncio.set_event_loop_policy(event_loop_policy)
    logger.debug("using %s event loop policy", event_loop_policy)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        logger.critical("main function encountered an exception: %s", error, exc_info=error)
        sys.exit(1)
