from dataclasses import dataclass

from shinshi.discord.interactables.models.option import Option


@dataclass
class AutocompleteOption(Option):
    is_autocomplete = True
