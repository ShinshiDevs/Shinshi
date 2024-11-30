from collections.abc import MutableSet
from typing import NamedTuple

from aurum.commands.base_command import BaseCommand


class Extension(NamedTuple):
    name: str
    commands: MutableSet[BaseCommand]
