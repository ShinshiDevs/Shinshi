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
from logging import getLogger
from typing import Dict, List, Sequence, Type

from hikari.applications import Application
from hikari.impl import SlashCommandBuilder

from shinshi.discord.bot import BaseBot
from shinshi.discord.converters import (
    OptionConverter,
    SlashCommandConverter,
    SubCommandConverter,
)
from shinshi.discord.workflows import WorkflowBase
from shinshi.discord.workflows.interactables.builders import (
    CommandGroupBuilder,
)
from shinshi.discord.workflows.interactables.commands import (
    Command,
    SlashCommand,
    SubCommand,
)
from shinshi.discord.workflows.interactables.group import Group
from shinshi.i18n import I18nProvider


class WorkflowManager:
    def __init__(
        self,
        bot: BaseBot,
        i18n_provider: I18nProvider,
        workflows: List[Type[WorkflowBase]],
    ) -> None:
        self.__logger = getLogger("shinshi.rest")
        self.bot = bot
        self.i18n_provider = i18n_provider
        self.workflows = workflows

        self._option_converter = OptionConverter(self.i18n_provider)
        self._slash_command_converter = SlashCommandConverter(
            self.bot,
            self.i18n_provider,
        )
        self._sub_command_converter = SubCommandConverter(self.bot, self.i18n_provider)

        self.slash_commands: Dict[str, SlashCommand] = {}
        self.groups: Dict[str, Group] = {}

        self.slash_commands_builders: List[SlashCommandBuilder] = []

    def __build_commands(self, commands: Sequence[Command]) -> None:
        for command in commands:
            if isinstance(command, SlashCommand):
                self.slash_commands[command.name] = command
                self.slash_commands_builders.append(
                    self._slash_command_converter.get_builder(command)
                )
            if isinstance(command, SubCommand):
                self.groups[command.group.name] = command.group

    def __build_groups(self) -> None:
        for group in self.groups.values():
            group_builder = CommandGroupBuilder(
                self.bot.rest.slash_command_builder,
                self._sub_command_converter,
                group,
            )
            self.slash_commands_builders.append(group_builder.build())

    async def build_workflows(self) -> None:
        for workflow_class in self.workflows:
            workflow: WorkflowBase = workflow_class()
            await workflow.start()

            self.__build_commands(workflow.get_commands())
        self.__build_groups()

    async def sync_slash_commands(self, application: Application) -> None:
        self.__logger.debug("Synchronization of slash commands...")
        commands = await self.bot.rest.set_application_commands(
            application, self.slash_commands_builders
        )
        self.__logger.debug(
            "Current commands: %s",
            ", ".join(f"{command.name} ({command.id})" for command in commands),
        )

    def get_command(
        self, group_name: str | None, subgroup_name: str | None, command_name: str
    ) -> Command | None:
        if group_name:
            return self.groups[group_name].get_command(subgroup_name, command_name)
        return self.slash_commands[command_name]
