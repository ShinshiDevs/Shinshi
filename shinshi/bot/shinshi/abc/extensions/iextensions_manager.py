from typing import Protocol, Type
from types import ModuleType
from collections.abc import Generator

from aurum.commands.base_command import BaseCommand

from shinshi.framework.extensions.extension import Extension


class IExtensionsManager(Protocol):
    def load_extension(self, module: ModuleType) -> Extension: ...

    def get_commands(self, module: ModuleType) -> Generator[Type[BaseCommand] | None, None, None]: ...
