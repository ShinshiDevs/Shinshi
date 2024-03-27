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
from shinshi.discord.workflows.interactables.commands.command import Command
from shinshi.discord.workflows.interactables.commands.slash_command import SlashCommand
from shinshi.discord.workflows.interactables.converters.convert_to_slash_command_builder import (
    convert_to_slash_command_builder,
)
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
            str, Tuple[WorkflowBase, SlashCommand, SlashCommandBuilder]
        ] = {}

    async def build_workflows(self) -> None:
        for workflow_class in self.workflows:
            workflow: WorkflowBase = workflow_class()
            await workflow.start()

            commands: List[Command] = workflow.get_commands()
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

    async def sync_slash_commands(self, application: Application) -> None:
        self.__logger.debug("Synchronization of slash commands...")
        slash_command_builders: List[SlashCommandBuilder] = []
        for _, _, builder in self.slash_commands.values():
            slash_command_builders.append(builder)
        commands = await self.bot.rest.set_application_commands(
            application, slash_command_builders
        )
        self.__logger.debug(
            "Current commands: %s",
            ", ".join(f"{command.name} ({command.id})" for command in commands),
        )
