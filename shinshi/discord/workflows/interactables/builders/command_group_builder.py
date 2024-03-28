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
from typing import Callable, List

from hikari.api import SlashCommandBuilder as APISlashCommandBuilder
from hikari.impl import SlashCommandBuilder as ImplSlashCommandBuilder

from shinshi.discord.workflows.interactables.commands.command import Command
from shinshi.discord.workflows.interactables.converters.convert_sub_command import (
    convert_sub_command,
)
from shinshi.discord.workflows.interactables.group import Group
from shinshi.i18n.i18n_provider import I18nProvider


class CommandGroupBuilder:
    def __init__(
        self,
        builder_factory: Callable[[str, str], APISlashCommandBuilder],
        i18n_provider: I18nProvider,
        group: Group,
        commands: List[Command],
    ) -> None:
        self.builder_factory = builder_factory
        self.i18n_provider = i18n_provider
        self.group = group
        self.commands = commands

    def build(self) -> ImplSlashCommandBuilder:
        builder_instance: APISlashCommandBuilder = (
            self.builder_factory(self.group.name, self.group.name)
            .set_default_member_permissions(self.group.default_member_permissions)
            .set_is_dm_enabled(self.group.is_dm_enabled)
            .set_is_nsfw(self.group.is_nsfw)
        )
        for command in self.commands:
            builder_instance.add_option(
                convert_sub_command(self.i18n_provider, command)
            )

        return builder_instance
