from os import getenv

from dotenv import load_dotenv
from hikari.presences import Activity

from shinshi import extensions
from shinshi.i18n import I18nProvider
from shinshi.sdk.bot import Bot
from shinshi.sdk.client import Client
from shinshi.utils.logging import setup_logging
from shinshi.utils.loop import install_uvloop
from shinshi.utils.version import get_version


def main() -> None:
    install_uvloop()
    setup_logging()
    load_dotenv()

    bot: Bot = Bot(getenv("SHINSHI_DISCORD_TOKEN"), banner=None)
    client: Client = Client(bot=bot, l10n=I18nProvider("i18n"))

    client.load_extensions(extensions.__name__, extensions.__path__)
    client.run(activity=Activity(name=f"v{get_version()}"))


if __name__ == "__main__":
    main()
