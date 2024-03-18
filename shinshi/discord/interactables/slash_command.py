from dataclasses import dataclass, field
from typing import Tuple

from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.models.option import Option
from shinshi.discord.interactables.models.translatable import Translatable


@dataclass(kw_only=True)
class SlashCommand(Command):
    description: Translatable

    group: str | None = None
    sub_group: str | None = None

    options: Tuple[Option, ...] = field(default_factory=tuple)
