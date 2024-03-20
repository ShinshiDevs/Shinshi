from dataclasses import dataclass, field
from typing import Tuple

from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.models.option import Option
from shinshi.discord.models.translatable import Translatable


@dataclass(kw_only=True)
class SlashCommand(Command):
    description: str | Translatable = "No description"

    group: Group | None = None
    sub_group: Group | None = None

    options: Tuple[Option, ...] = field(default_factory=tuple)
