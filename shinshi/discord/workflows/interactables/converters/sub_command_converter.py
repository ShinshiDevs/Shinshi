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

from hikari import CommandOption, OptionType

from shinshi.discord.bot.base_bot import BaseBot
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands.sub_command import SubCommand
from shinshi.discord.workflows.interactables.converters.option_converter import (
    OptionConverter,
)
from shinshi.i18n.i18n_provider import I18nProvider


class SubCommandConverter:
    def __init__(
        self,
        bot: BaseBot,
        i18n_provider: I18nProvider,
    ) -> None:
        self.bot = bot
        self.i18n_provider = i18n_provider
        self.option_converter = OptionConverter(self.i18n_provider)

    def convert(self, command: SubCommand) -> CommandOption:
        description_localizations: Dict[str, str] | None = None
        if isinstance(command.description, Translatable):
            description_localizations = command.description.build(self.i18n_provider)
        return CommandOption(
            type=OptionType.SUB_COMMAND,
            name=command.name,
            description=(
                getattr(command.description, "fallback", command.description)
                or "No description"
            ),
            options=(
                self.option_converter.convert(option) for option in command.options
            ),
            description_localizations=description_localizations,
        )
