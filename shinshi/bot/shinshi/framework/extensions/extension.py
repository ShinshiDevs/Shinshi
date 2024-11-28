from typing import MutableSet, NamedTuple

from aurum.commands.base_command import BaseCommand


class Extension(NamedTuple):
    name: str
    commands: MutableSet[BaseCommand]
