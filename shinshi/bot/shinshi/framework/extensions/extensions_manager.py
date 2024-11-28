from pkgutil import iter_modules
from importlib import import_module
from types import ModuleType
from typing import Type, Dict
from collections.abc import Generator, Sequence
from logging import Logger, getLogger

from aurum.commands.base_command import BaseCommand

from shinshi.abc.bot.ibot_service import IBotService
from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.abc.kernel.types.kernel_aware import KernelAware
from shinshi.framework.commands.command_handler import CommandHandler
from shinshi.framework.extensions.extension import Extension


class ExtensionsManager(KernelAware):
    __slots__: Sequence[str] = ("__logger", "commands", "module", "extensions")

    def __init__(
        self, bot_service: IBotService, i18n_provider: II18nProvider, *, module: ModuleType, sync_commands: bool = True
    ) -> None:
        self.__logger: Logger = getLogger("shinshi.extensions")

        self.commands: CommandHandler = CommandHandler(bot_service.bot, i18n_provider, sync_commands=sync_commands)
        self.module: ModuleType = module

        self.extensions: Dict[str, Extension] = {}

    async def start(self) -> None:
        self.__logger.debug("starting, loading extensions from %s", self.module.__name__)
        for _, extension_name, _ in iter_modules(self.module.__path__):
            module: ModuleType | None = import_module(f"{self.module.__name__}.{extension_name}")
            try:
                extension: Extension = self.load_extension(module)
            except Exception as error:
                self.__logger.error("cannot load extension %s due unexcepted error", module.__name__, exc_info=error)
                continue
            self.extensions[extension.name] = extension
            self.__logger.debug("load extension %s", extension.name)
        self.__logger.info("loaded %s extensions", len(self.extensions))
        for extension in self.extensions.values():
            self.commands.commands.update({command.name: command for command in extension.commands})
        await self.commands.start()

    async def stop(self) -> None:
        self.extensions.clear()

    def load_extension(self, module: ModuleType) -> Extension:
        extension: Extension = Extension(name=module.__name__, commands=set())
        for command in self.get_commands(module):
            extension.commands.add(command())  # type: ignore  # TODO: services injection
        return extension

    def get_commands(self, module: ModuleType) -> Generator[Type[BaseCommand] | None, None, None]:
        commands_module: ModuleType | None = import_module(f"{module.__name__}.commands")
        if not commands_module:
            self.__logger.warning("coundn't find a commands module in %s", module.__name__)
            return
        for command_class in commands_module.__all__:
            yield getattr(commands_module, command_class)
