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
from typing import Callable

from hikari.api import SlashCommandBuilder as APISlashCommandBuilder
from hikari.commands import CommandOption, OptionType
from hikari.impl import SlashCommandBuilder as ImplSlashCommandBuilder

from shinshi.discord.converters import SubCommandConverter
from shinshi.discord.workflows.interactables.commands import SubCommand
from shinshi.discord.workflows.interactables.group import Group


class CommandGroupBuilder:
    def __init__(
        self,
        builder_factory: Callable[[str, str], APISlashCommandBuilder],
        converter: SubCommandConverter,
        group: Group,
    ) -> None:
        self.builder_factory = builder_factory
        self.sub_command_converter = converter
        self.group = group

    def build(self) -> ImplSlashCommandBuilder:
        builder_instance: APISlashCommandBuilder = (
            self.builder_factory(self.group.name, self.group.name)
            .set_default_member_permissions(self.group.default_member_permissions)
            .set_is_dm_enabled(self.group.is_dm_enabled)
            .set_is_nsfw(self.group.is_nsfw)
        )
        for name, entity in self.group.commands.items():
            if isinstance(entity, SubCommand):
                builder_instance.add_option(self.sub_command_converter.convert(entity))
            if isinstance(entity, dict):
                sub_group: CommandOption = CommandOption(
                    type=OptionType.SUB_COMMAND_GROUP,
                    name=name,
                    description=name,
                    options=(
                        self.sub_command_converter.convert(sub_command)
                        for sub_command in entity.values()
                    ),
                )
                builder_instance.add_option(sub_group)
        return builder_instance
