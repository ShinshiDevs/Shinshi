from hikari.presences import Activity, ActivityType

from shinshi import __version__
from shinshi.client import Shinshi
from shinshi.dotenv import load_dotenv
from shinshi.l10n import LocalizationProvider
from shinshi.utils.loop import install_uvloop

if __name__ == "__main__":
    load_dotenv()
    install_uvloop()

    client: Shinshi = Shinshi(l10n=LocalizationProvider("i18n"))
    client.run(
        activity=Activity(
            type=ActivityType.LISTENING,
            name=f"v{__version__}",
        )
    )
