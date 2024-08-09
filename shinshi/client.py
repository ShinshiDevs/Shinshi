from os import environ
from aurum.commands.enum import SyncCommandsFlag
from aurum.l10n import LocalizationProviderInterface
from aurum.client import Client as AurumClient

from shinshi.bot import Bot


class Client(AurumClient):
    def __init__(
        self,
        l10n: LocalizationProviderInterface,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
    ) -> None:
        self.bot: Bot = Bot(environ.get("SHINSHI_DISCORD_TOKEN"))
        super().__init__(bot=self.bot, l10n=l10n, sync_commands=sync_commands)

    def run(self, **kwargs) -> None:
        self.bot.run(**kwargs)
