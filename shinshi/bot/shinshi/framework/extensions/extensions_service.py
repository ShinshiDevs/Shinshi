from importlib import import_module
from logging import Logger, getLogger
from pkgutil import iter_modules
from typing import Sequence

from aurum.client import Client
from aurum.commands.app_command import AppCommand

from shinshi.abc.bot.ibot_service import IBotService
from shinshi.abc.extensions.iextensions_service import IExtensionsService
from shinshi.framework.extensions.extension import Extension


class ExtensionsService(IExtensionsService):
    def __init__(
        self,
        bot_service: IBotService,
        extensions_package: str,
        extensions_path: str,
        *,
        sync_commands: bool = True,
    ) -> None:
        self.__logger: Logger = getLogger("shinshi.extensions")

        self.client: Client = bot_service.client
        self.extensions_package: str = extensions_package
        self.extensions_path: str = extensions_path

        self.sync_commands: bool = sync_commands

        self.extensions: dict[str, Extension] = {}

    async def start(self) -> None:
        for _, extension_name, _ in iter_modules(self.extensions_path):
            try:
                extension = self.extensions[extension_name] = Extension(
                    name=extension_name,
                    package=f"{self.extensions_package}.{extension_name}",
                )
                commands_package: Sequence[str] = import_module(f"{extension.package}.commands")
                for command_class in commands_package.__all__:  # command_class is a name of command class
                    command: AppCommand = getattr(commands_package, command_class)()
                    extension.commands[command.name] = command
                self.__logger.debug("loaded extension %s", extension_name)
            except Exception as error:
                self.__logger.error(
                    "failed to load extension %s: %s", extension_name, error, exc_info=error
                )
        if self.sync_commands:
            for extension in self.extensions.values():
                self.client.commands.commands.update(extension.commands)
            await self.client.commands.sync()

    async def stop(self) -> None:
        self.extensions.clear()
