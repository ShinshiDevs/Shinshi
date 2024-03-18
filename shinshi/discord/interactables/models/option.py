from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from hikari.commands import OptionType

from shinshi.discord.interactables.models.choice import Choice
from shinshi.discord.interactables.models.translatable import Translatable


@dataclass
class Option:
    type: OptionType

    name: str
    description: Translatable

    choices: Tuple[Choice, ...] = field(default_factory=tuple)

    required: bool = True
    is_autocomplete: bool = False
