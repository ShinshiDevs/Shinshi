from importlib import import_module
from logging import Logger, getLogger
from pkgutil import iter_modules
from types import ModuleType
from typing import Any, Callable, Sequence

from aurum.client import Client
from aurum.commands.app_command import AppCommand

from shinshi.abc.bot.ibot_service import IBotService
from shinshi.abc.extensions.extension import Extension
from shinshi.abc.extensions.iextensions_service import IExtensionsService
from shinshi.abc.kernel.types.kernel_aware import KernelAware
from shinshi.abc.services.iservice import IService


class ExtensionsService(IExtensionsService, KernelAware):
    __slots__: Sequence[str] = (
        "__logger",
        "client",
        "extensions_package",
        "extensions_path",
        "sync_commands",
        "extensions",
    )

    def __init__(
        self, bot_service: IBotService, extensions_package: str, extensions_path: str, *, sync_commands: bool = True
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
                    name=extension_name, package=f"{self.extensions_package}.{extension_name}"
                )
                commands_package: ModuleType = import_module(f"{extension.package}.commands")
                for command_class_name in commands_package.__all__:
                    command_class: type[AppCommand] = getattr(commands_package, command_class_name)  # just class
                    command: AppCommand = command_class(
                        **self.inject_dependencies(command_class.__init__)
                    )  # inited command object
                    extension.commands[command.name] = command
                self.__logger.debug("loaded extension %s", extension_name)
            except Exception as error:  # pylint: disable=W0718
                self.__logger.error("failed to load extension %s: %s", extension_name, error, exc_info=error)
        if self.sync_commands:
            for extension in self.extensions.values():
                self.client.commands.commands.update(extension.commands)
            await self.client.commands.sync()

    async def stop(self) -> None:
        self.extensions.clear()

    def inject_dependencies(self, func: Callable[..., None]) -> dict[str, Any]:
        dependencies: dict[str, Any] = func.__annotations__.copy()
        dependencies.pop("return", None)  # removing return annotation `-> None`

        for name, annotation in dependencies.items():
            # annotation meant do be interface of service
            assert issubclass(annotation, IService)
            dependencies[name] = self.kernel.get_service(annotation, None)

        return dependencies
