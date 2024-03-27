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
from typing import Callable, Dict, Tuple

from hikari.api import SlashCommandBuilder as APISlashCommandBuilder
from hikari.impl import SlashCommandBuilder as ImplSlashCommandBuilder

from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.interactables.commands.slash_command import SlashCommand
from shinshi.i18n.i18n_provider import I18nProvider


def convert_to_slash_command_builder(
    builder: Callable[[str, str], APISlashCommandBuilder],
    i18n_provider: I18nProvider,
    command: SlashCommand,
) -> ImplSlashCommandBuilder:
    description: str | Tuple[str, Dict[str, str]] | None = None
    if isinstance(command.description, Translatable):
        description = command.description.build(i18n_provider)
    builder_instance: APISlashCommandBuilder = builder(
        command.name, description[0] if isinstance(description, tuple) else description
    )
    if isinstance(command.description, Translatable):
        builder_instance.set_description_localizations(description[1])
    builder_instance.set_default_member_permissions(command.default_member_permissions)
    builder_instance.set_is_dm_enabled(command.is_dm_enabled)
    builder_instance.set_is_nsfw(command.is_nsfw)
    return builder_instance
