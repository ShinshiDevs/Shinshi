import asyncio

from dotenv import load_dotenv

from shinshi import extensions
from shinshi.framework.bot.bot_service import BotService
from shinshi.framework.database.database_service import DatabaseService
from shinshi.framework.extensions.extensions_service import ExtensionsService
from shinshi.framework.i18n.i18n_provider import I18nProvider
from shinshi.framework.kernel import Kernel
from shinshi.utils.logging import setup_logging
from shinshi.utils.loop import get_event_loop_policy


async def main() -> None:
    setup_logging()
    load_dotenv(verbose=True, override=True)

    i18n_provider: I18nProvider = I18nProvider("resources/i18n")
    database_service: DatabaseService = DatabaseService("shinshi.abc.database.models")
    bot_service: BotService = BotService()
    extensions_service: ExtensionsService = ExtensionsService(
        bot_service, extensions.__name__, extensions.__path__
    )

    await Kernel(
        i18n_provider,
        database_service,
        bot_service,
        extensions_service,
    ).run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(get_event_loop_policy())
    asyncio.run(main())
