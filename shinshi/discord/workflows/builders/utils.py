from hikari import Locale, CommandChoice, CommandOption

from shinshi.discord.interactables.models.channel_option import ChannelOption
from shinshi.discord.interactables.models.number_option import NumberOption
from shinshi.discord.interactables.models.option import Option
from shinshi.discord.interactables.models.string_option import StringOption
from shinshi.discord.interactables.models.translatable import Translatable
from shinshi.i18n import I18nProvider


def convert_option(option: Option, i18n: I18nProvider) -> CommandOption:
    return CommandOption(
        type=option.type,
        name=option.name,
        description=option.description.translate(i18n)[Locale.EN_US],
        description_localizations=option.description.translate(i18n),
        is_required=option.is_required,
        autocomplete=option.autocomplete,
        choices=(
            CommandChoice(
                name=(
                    choice.name.translate(i18n)[Locale.EN_US]
                    if isinstance(choice.name, Translatable) else choice.name
                ),
                name_localizations=(
                    choice.name.translate(i18n)
                    if isinstance(choice.name, Translatable) else None
                ),
                value=choice.value,
            )
            for choice in option.choices
        ) if not option.autocomplete else (),
        max_length=option.max_length if isinstance(option, StringOption) else None,
        min_length=option.max_length if isinstance(option, StringOption) else None,
        max_value=option.max_value if isinstance(option, NumberOption) else None,
        min_value=option.min_value if isinstance(option, NumberOption) else None,
        channel_types=option.channel_types if isinstance(option, ChannelOption) else (),
    )
