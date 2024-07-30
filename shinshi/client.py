from os import environ
from aurum.l10n import LocalizationProviderInterface
from aurum.client import Client as AurumClient
from hikari.impl import GatewayBot


class Client(AurumClient):
    def __init__(
        self,
        l10n: LocalizationProviderInterface,
    ) -> None:
        self.bot: GatewayBot = GatewayBot(environ.get("SHINSHI_DISCORD_TOKEN"))
        super().__init__(bot=self.bot, l10n=l10n)

    def run(self, **kwargs) -> None:
        self.bot.run(**kwargs)
