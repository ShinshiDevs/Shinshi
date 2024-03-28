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

from hikari import OptionType
from hikari.commands import CommandOption

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands.slash_command import SlashCommand
from shinshi.discord.workflows.interactables.converters.convert_option import (
    convert_option,
)
from shinshi.i18n.i18n_provider import I18nProvider


def convert_sub_command(
    i18n_provider: I18nProvider,
    command: SlashCommand,
) -> CommandOption:
    description_localizations: Dict[str, str] | None = None
    if isinstance(command.description, Translatable):
        description_localizations = command.description.build(i18n_provider)

    return CommandOption(
        type=OptionType.SUB_COMMAND,
        name=command.name,
        description=(
            getattr(command.description, "fallback", command.description)
            or "No description"
        ),
        options=(convert_option(i18n_provider, option) for option in command.options),
        description_localizations=description_localizations,
    )
