from collections.abc import Generator
from types import ModuleType
from typing import Protocol

from aurum.commands.base_command import BaseCommand

from shinshi.framework.extensions.extension import Extension


class IExtensionsManager(Protocol):
    def load_extension(self, module: ModuleType) -> Extension: ...

    def get_commands(self, module: ModuleType) -> Generator[type[BaseCommand] | None, None, None]: ...
