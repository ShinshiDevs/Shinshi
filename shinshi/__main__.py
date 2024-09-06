from logging import DEBUG

from hikari.presences import Activity

from shinshi import __version__, extensions
from shinshi.client import Client
from shinshi.dotenv import load_dotenv
from shinshi.l10n import LocalizationProvider
from shinshi.utils.logging import setup_logging
from shinshi.utils.loop import install_uvloop

if __name__ == "__main__":
    load_dotenv()
    setup_logging(level=DEBUG)
    install_uvloop()

    client: Client = Client(l10n=LocalizationProvider("i18n"))
    client.load_extensions(extensions.__name__, extensions.__path__)
    client.run(
        activity=Activity(
            name=f"v{__version__}",
        )
    )
