from os import environ
from aurum import LocalizationProviderInterface
from aurum.client import Client
from hikari.impl import GatewayBot


class Shinshi(Client):
    def __init__(
        self,
        l10n: LocalizationProviderInterface,
    ) -> None:
        self.bot: GatewayBot = GatewayBot(environ.get("SHINSHI_DISCORD_TOKEN"))
        super().__init__(bot=self.bot, l10n=l10n)

    def run(self, *args, **kwargs) -> None:
        self.bot.run(*args, **kwargs)
