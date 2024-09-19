from collections.abc import Sequence
from importlib import import_module
from pkgutil import iter_modules

from aurum.client import Client as AurumClient
from aurum.commands.app_command import AppCommand


class Client(AurumClient):
    __slots__: Sequence[str] = ()

    def load_extensions(self, module_name: str, module_path: str) -> None:
        """Load extensions from module."""
        for _, extension, _ in iter_modules(module_path):
            commands = import_module(f"{module_name}.{extension}.commands")
            for name in getattr(commands, "__all__"):
                command: AppCommand = getattr(commands, name)()
                self.commands.commands[command.name] = command
            self.__logger.debug("loaded extension %s", extension)

    def run(self, **kwargs) -> None:
        self.__logger.info("starting")
        self.bot.run(**kwargs)
