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

from hikari.api import SlashCommandBuilder as APISlashCommandBuilder
from hikari.impl import SlashCommandBuilder as ImplSlashCommandBuilder

from shinshi.discord.bot import BaseBot
from shinshi.discord.converters import OptionConverter
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands import SlashCommand
from shinshi.i18n import I18nProvider


class SlashCommandConverter:
    def __init__(
        self,
        bot: BaseBot,
        i18n_provider: I18nProvider,
    ) -> None:
        self.bot = bot
        self.i18n_provider = i18n_provider
        self.option_converter = OptionConverter(self.i18n_provider)

    def get_builder(self, command: SlashCommand) -> ImplSlashCommandBuilder:
        description_localizations: Dict[str, str] | None = None
        if isinstance(command.description, Translatable):
            description_localizations = command.description.build(self.i18n_provider)
        builder_instance: APISlashCommandBuilder = (
            self.bot.rest.slash_command_builder(
                command.name,
                getattr(command.description, "fallback", command.description)
                or "No description",
            )
            .set_description_localizations(description_localizations)
            .set_default_member_permissions(command.default_member_permissions)
            .set_is_dm_enabled(command.is_dm_enabled)
            .set_is_nsfw(command.is_nsfw)
        )
        for option in command.options:
            builder_instance.add_option(self.option_converter.convert(option))

        return builder_instance
