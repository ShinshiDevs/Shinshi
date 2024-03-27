# Copyright (C) 2024 Shinshi Developers Team
#
# This file is part of Shinshi.
#
# Shinshi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinshi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Shinshi.  If not, see <https://www.gnu.org/licenses/>.
from typing import Dict

from hikari.commands import CommandOption

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.converters.convert_choice import (
    convert_choice,
)
from shinshi.discord.workflows.interactables.options.option import Option
from shinshi.i18n.i18n_provider import I18nProvider


def convert_option(i18n_provider: I18nProvider, option: Option) -> CommandOption:
    description_localizations: Dict[str, str] | None = None
    if isinstance(option.description, Translatable):
        description_localizations = option.description.build(i18n_provider)
    return CommandOption(
        type=option.type,
        name=option.name,
        description=(
            getattr(option.description, "fallback", option.description)
            or "No description"
        ),
        description_localizations=description_localizations,
        is_required=option.is_required,
        autocomplete=option.is_autocomplete,
        choices=(convert_choice(i18n_provider, choice) for choice in option.choices),
        max_length=getattr(option, "max_length", None),
        min_length=getattr(option, "min_length", None),
        max_value=getattr(option, "max_value", None),
        min_value=getattr(option, "min_value", None),
        channel_types=getattr(option, "channel_types", None),
    )
