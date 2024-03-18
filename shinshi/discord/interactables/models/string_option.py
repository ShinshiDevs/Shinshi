from dataclasses import dataclass

from shinshi.discord.interactables.models.option import Option


@dataclass
class StringOption(Option):
    min_length: int | None = None
    max_length: int | None = None
