from collections.abc import Sequence
from importlib import import_module
from pkgutil import iter_modules

from aurum.client import Client as AurumClient
from aurum.commands.app_command import AppCommand

from shinshi.sdk.event import Event


class Client(AurumClient):
    __slots__: Sequence[str] = ()

    def load_extensions(self, module_name: str, module_path: str) -> None:
        """Load extensions from module."""
        for _, extension, _ in iter_modules(module_path):
            module = import_module(f"{module_name}.{extension}.commands")
            for name in getattr(module, "__all__"):
                command: AppCommand = getattr(module, name)()
                self.commands.commands[command.name] = command
            self.__logger.debug("loaded extension %s", extension)

    def load_events(self, module_name: str) -> None:
        module = import_module(module_name)
        for event in module.__all__:
            event: Event = getattr(module, event)
            self.bot.event_manager.subscribe(event.event_type(), event.callback)

    def run(self, **kwargs) -> None:
        self.__logger.info("starting")
        self.bot.run(**kwargs)
