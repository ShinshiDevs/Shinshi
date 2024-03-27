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
from typing import Any, Dict

from hikari.commands import CommandOption, CommandType, OptionType
from hikari.interactions.base_interactions import PartialInteraction
from hikari.interactions.command_interactions import CommandInteraction

from shinshi.discord.bot.base_bot import BaseBot
from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.workflows.interactables.commands.slash_command import SlashCommand
from shinshi.discord.workflows.interactables.interactable import Interactable
from shinshi.discord.workflows.workflow_base import WorkflowBase
from shinshi.discord.workflows.workflow_manager import WorkflowManager
from shinshi.i18n.i18n_provider import I18nProvider

_DEFAULT_LANGUAGE: str = "en-US"


class InteractionProcessor:
    def __init__(
        self,
        bot: BaseBot,
        i18n_provider: I18nProvider,
        workflow_manager: WorkflowManager,
    ) -> None:
        self.__logger = getLogger("shinshi.interactions")
        self.bot = bot
        self.i18n_provider = i18n_provider
        self.workflow_manager = workflow_manager

    async def __proceed_slash_command(self, interaction: CommandInteraction) -> None:
        group_name, subgroup_name, command_name = None, None, interaction.command_name
        arguments: Dict[str, Any] = {}
        options: list[CommandOption] = (
            list(interaction.options) if interaction.options else []
        )
        while options:
            option = options.pop(0)
            match option.type:
                case OptionType.SUB_COMMAND_GROUP:
                    group_name = interaction.command_name
                    subgroup_name = option.name
                    options = list(option.options) if option.options else []
                case OptionType.SUB_COMMAND:
                    group_name = group_name or interaction.command_name
                    command_name = option.name
                    options = list(option.options) if option.options else []
                case _:
                    arguments[option.name] = option.value

        workflow, command = None, None
        if group_name is not None:
            if subgroup_name is not None:
                workflow, command, _ = self.workflow_manager.sub_groups[group_name][
                    subgroup_name
                ][command_name]
            else:
                workflow, command, _ = self.workflow_manager.groups[group_name][
                    command_name
                ]
        else:
            workflow, command, _ = self.workflow_manager.slash_commands[command_name]
        context = await self.create_interaction_context(interaction, command)
        await self.__execute_slash_command(context, workflow, command, arguments)

    async def __execute_slash_command(
        self,
        context: InteractionContext,
        workflow: WorkflowBase,
        interactable: SlashCommand,
        arguments: Dict[str, Any],
    ) -> None:
        try:
            await self.__execute_hooks(context, interactable)
            if interactable.is_defer:
                await context.defer()
            await interactable.callback(
                workflow,
                context,
                **arguments,
            )
        except Exception as exception:
            self.__logger.error(
                "error occurred while executing slash-command %s.",
                interactable.name,
                exc_info=exception,
            )

    async def __execute_hooks(
        self, context: InteractionContext, interactable: SlashCommand
    ) -> None:
        for hook in interactable.hooks or ():
            await hook(context)

    async def create_interaction_context(
        self, interaction: PartialInteraction, interactable: Interactable
    ) -> InteractionContext:
        return InteractionContext(
            interaction=interaction,
            bot=self.bot,
            i18n=(
                self.i18n_provider.languages.get(
                    str(interaction.locale or interaction.guild_locale), None
                )
                or self.i18n_provider.languages.get(_DEFAULT_LANGUAGE)
            ),
            interactable=interactable,
        )

    async def proceed(self, interaction: PartialInteraction) -> None:
        if isinstance(interaction, CommandInteraction):
            if interaction.command_type is CommandType.SLASH:
                await self.__proceed_slash_command(interaction)
