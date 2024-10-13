from __future__ import annotations

from importlib import import_module
from logging import Logger, getLogger
from pkgutil import iter_modules
from typing import TYPE_CHECKING, Sequence

from aurum.commands.app_command import AppCommand

from shinshi.types.extension import Extension

if TYPE_CHECKING:
    from shinshi.bot.client import Client


class ExtensionManager:
    __slots__: Sequence[str] = ("__logger", "client", "extensions")

    def __init__(self, client: Client) -> None:
        self.__logger: Logger = getLogger(__name__)

        self.client: Client = client
        self.extensions: dict[str, Extension] = {}

    def load_extensions(self, module_name: str, module_path: str) -> None:
        for _, extension_name, _ in iter_modules(module_path):
            try:
                self.extensions[extension_name] = Extension(
                    name=extension_name,
                    commands=import_module(f"{module_name}.{extension_name}.commands"),
                )
                self.__logger.debug("saved extension: %s", extension_name)
            except Exception as exception:
                self.__logger.error(
                    "Failed to load extension %s: %s", extension_name, exception
                )

    async def sync_commands(self) -> None:
        for extension_name, extension in self.extensions.items():
            commands = extension["commands"]
            for command_name in commands.__all__:
                if hasattr(commands, command_name):
                    command: AppCommand = getattr(commands, command_name)()
                    self.client.add_command(command)
                    self.__logger.debug(
                        "registered command: %s from extension: %s",
                        command.name,
                        extension_name,
                    )
                else:
                    self.__logger.warning(
                        "command %s not found in module %s",
                        command_name,
                        extension_name,
                    )
