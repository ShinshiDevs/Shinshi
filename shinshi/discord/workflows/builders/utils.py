from typing import Dict

from hikari import CommandChoice, CommandOption

from shinshi.discord.interactables.models.channel_option import ChannelOption
from shinshi.discord.interactables.models.choice import Choice
from shinshi.discord.interactables.models.number_option import NumberOption
from shinshi.discord.interactables.models.option import Option
from shinshi.discord.interactables.models.string_option import StringOption
from shinshi.discord.models.translatable import Translatable
from shinshi.i18n import I18nProvider


def convert_option_choice(choice: Choice, i18n: I18nProvider) -> CommandChoice:
    names: Dict[str, str] | None = None
    if isinstance(choice.name, Translatable):
        names = choice.name.translate(i18n)
    return CommandChoice(
        name=getattr(choice.name, "fallback", choice.name),
        name_localizations=names,
        value=choice.value
    )


def convert_option(option: Option, i18n: I18nProvider) -> CommandOption:
    descriptions: Dict[str, str] | None = None
    if isinstance(option.description, Translatable):
        descriptions = option.description.translate(i18n)
    return CommandOption(
        type=option.type,
        name=option.name,
        description=getattr(option.description, "fallback", option.description),
        description_localizations=descriptions,
        is_required=option.is_required,
        autocomplete=option.is_autocomplete,
        choices=(
            convert_option_choice(choice, i18n) for choice in option.choices
        ) if not option.is_autocomplete else (),
        max_length=option.max_length if isinstance(option, StringOption) else None,
        min_length=option.max_length if isinstance(option, StringOption) else None,
        max_value=option.max_value if isinstance(option, NumberOption) else None,
        min_value=option.min_value if isinstance(option, NumberOption) else None,
        channel_types=option.channel_types if isinstance(option, ChannelOption) else (),
    )
