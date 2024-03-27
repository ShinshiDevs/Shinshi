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
from typing import List, Type

from hikari.commands import CommandType, OptionType
from hikari.interactions.base_interactions import PartialInteraction
from hikari.interactions.command_interactions import CommandInteraction

from shinshi.discord.bot.base_bot import BaseBot
from shinshi.discord.models.interaction_context import InteractionContext
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
        options_types: List[Type[OptionType]] = list(
            option.type for option in interaction.options
        )
        if not any(
            OptionType.SUB_COMMAND in options_types
            or OptionType.SUB_COMMAND_GROUP in options_types
        ):
            workflow, command, _ = self.workflow_manager.slash_commands[
                interaction.command_name
            ]
            context = InteractionContext(
                interaction=interaction,
                bot=self.bot,
                i18n=self.i18n_provider.languages.get(
                    str(interaction.locale or interaction.guild_locale),
                    self.i18n_provider.languages.get(_DEFAULT_LANGUAGE),
                ),
                interactable=command,
            )
            if command.hooks:
                for hook in command.hooks:
                    await hook.callback(context)
            if command.is_defer:
                await context.defer()
            try:
                await command.callback(
                    workflow,
                    context,
                    **{option.name: option.value for option in interaction.options},
                )
            except Exception as exception:
                self.__logger.error(
                    "error occurred while executing slash-command %s.",
                    command.name,
                    exc_info=exception,
                )

    async def proceed(self, interaction: PartialInteraction) -> None:
        if isinstance(interaction, CommandInteraction):
            if interaction.command_type is CommandType.SLASH:
                await self.__proceed_slash_command(interaction)
