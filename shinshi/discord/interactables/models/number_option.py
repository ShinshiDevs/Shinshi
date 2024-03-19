from dataclasses import dataclass

from shinshi.discord.interactables.models.option import Option


@dataclass
class NumberOption(Option):
    min_value: int | None = None
    max_value: int | None = None
