from dataclasses import dataclass

from shinshi.discord.models.translatable import Translatable


@dataclass
class Choice:
    name: Translatable | str
    value: str | float | int
