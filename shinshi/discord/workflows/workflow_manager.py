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
from typing import Dict, List, Tuple, Type

from hikari.applications import Application
from hikari.impl import SlashCommandBuilder

from shinshi.discord.bot.base_bot import BaseBot
from shinshi.discord.workflows.interactables.builders.command_group_builder import (
    CommandGroupBuilder,
)
from shinshi.discord.workflows.interactables.commands.command import Command
from shinshi.discord.workflows.interactables.commands.slash_command import SlashCommand
from shinshi.discord.workflows.interactables.commands.sub_command import SubCommand
from shinshi.discord.workflows.interactables.converters.convert_to_slash_command_builder import (
    convert_to_slash_command_builder,
)
from shinshi.discord.workflows.interactables.group import Group
from shinshi.discord.workflows.workflow_base import WorkflowBase
from shinshi.i18n.i18n_provider import I18nProvider


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

        self.slash_commands: Dict[
            str,
            Tuple[WorkflowBase, SlashCommand, SlashCommandBuilder],
        ] = {}

        self.groups: Dict[
            str,
            Tuple[Dict[str, Tuple[WorkflowBase, SlashCommand]], SlashCommandBuilder],
        ] = {}

    async def build_workflows(self) -> None:
        groups: Dict[str, Group] = {}
        groups_to_build: Dict[str, List[SlashCommand]] = {}

        for workflow_class in self.workflows:
            workflow: WorkflowBase = workflow_class()
            await workflow.start()

            commands: List[Command | SubCommand] = workflow.get_commands()
            for command in commands:
                if isinstance(command, SlashCommand):
                    self.slash_commands[command.name] = (
                        workflow,
                        command,
                        convert_to_slash_command_builder(
                            self.bot.rest.slash_command_builder,
                            self.i18n_provider,
                            command,
                        ),
                    )
                if isinstance(command, SubCommand):
                    if command.group:
                        if command.sub_group:
                            ...
                        else:
                            groups_to_build.setdefault(command.group.name, []).append(
                                command
                            )
                            groups[command.group.name] = command.group

        for group_name, commands in groups_to_build.items():
            group: Group = groups[group_name]
            group_builder = CommandGroupBuilder(
                self.bot.rest.slash_command_builder,
                self.i18n_provider,
                group,
                commands,
            )
            children: Dict[str, Tuple[WorkflowBase, SlashCommand]] = {
                command.name: (workflow, command) for command in commands
            }
            self.groups[group_name] = (children, group_builder.build())

    async def sync_slash_commands(self, application: Application) -> None:
        self.__logger.debug("Synchronization of slash commands...")
        slash_command_builders: List[SlashCommandBuilder] = []
        for _, _, builder in self.slash_commands.values():
            slash_command_builders.append(builder)
        for _, builder in self.groups.values():
            slash_command_builders.append(builder)
        commands = await self.bot.rest.set_application_commands(
            application, slash_command_builders
        )
        self.__logger.debug(
            "Current commands: %s",
            ", ".join(f"{command.name} ({command.id})" for command in commands),
        )

    def get_command(
        self, group_name: str | None, subgroup_name: str | None, command_name: str
    ) -> Tuple[WorkflowBase, SlashCommand] | None:
        if group_name:
            if subgroup_name:
                workflow, command = self.sub_groups[group_name][subgroup_name][0][
                    command_name
                ]
            else:
                workflow, command = self.groups[group_name][0][command_name]
        else:
            workflow, command, _ = self.slash_commands[command_name]
        return workflow, command
