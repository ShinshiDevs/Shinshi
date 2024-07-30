from hikari.presences import Activity

from shinshi import __version__
from shinshi.client import Client
from shinshi.dotenv import load_dotenv
from shinshi.l10n import LocalizationProvider
from shinshi.utils.loop import install_uvloop

if __name__ == "__main__":
    install_uvloop()
    load_dotenv()

    client: Client = Client(l10n=LocalizationProvider("i18n"))
    client.run(
        activity=Activity(
            name=f"v{__version__}",
        )
    )
