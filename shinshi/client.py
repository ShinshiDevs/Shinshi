import os
from collections.abc import Sequence
from importlib import import_module
from logging import Logger, getLogger
from pkgutil import iter_modules

from aurum.client import Client as AurumClient
from aurum.commands.app_command import AppCommand
from aurum.commands.enum import SyncCommandsFlag
from aurum.l10n import LocalizationProviderInterface

from shinshi.bot import Bot


class Client(AurumClient):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        l10n: LocalizationProviderInterface,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
    ) -> None:
        super().__init__(
            bot=Bot(os.environ.get("SHINSHI_DISCORD_TOKEN"), banner=None),  # idk is it normal or not
            l10n=l10n,
            sync_commands=sync_commands,
        )
        self.__logger: Logger = getLogger("shinshi.client")

    def load_extensions(self, module_name: str, module_path: str) -> None:
        """Load extensions from module."""
        for _, extension, _ in iter_modules(module_path):
            commands = import_module(f"{module_name}.{extension}.commands")
            for name in getattr(commands, "__all__"):
                command: AppCommand = getattr(
                    commands, name
                )()  # init an object of command
                self.commands.commands[command.name] = command
            self.__logger.debug("loaded extension %s", extension)

    def run(self, **kwargs) -> None:
        self.__logger.info("starting")
        self.bot.run(**kwargs)
