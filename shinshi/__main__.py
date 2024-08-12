from colorlog import DEBUG, basicConfig
from hikari.presences import Activity

from shinshi import __version__, extensions
from shinshi.client import Client
from shinshi.dotenv import load_dotenv
from shinshi.l10n import LocalizationProvider
from shinshi.utils.loop import install_uvloop

if __name__ == "__main__":
    basicConfig(level=DEBUG, format="%(log_color)s%(levelname)-8s%(reset)s %(message)s")

    install_uvloop()
    load_dotenv()

    client: Client = Client(l10n=LocalizationProvider("i18n"))
    client.load_extensions(extensions.__name__, extensions.__path__)
    client.run(
        activity=Activity(
            name=f"v{__version__}",
        )
    )
