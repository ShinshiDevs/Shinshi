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
from typing import Any, Dict, List

from hikari.commands import CommandOption, OptionType
from hikari.interactions import CommandInteraction

from shinshi.discord.interactables.command import Command
from shinshi.discord.processors.command_processor import CommandProcessor


class SlashCommandProcessor(CommandProcessor):
    __logger = getLogger("shinshi.interactions")

    async def proceed_slash_command(self, interaction: CommandInteraction) -> None:
        group_name, subgroup_name, command_name = None, None, interaction.command_name
        arguments: Dict[str, Any] = {}
        options: List[CommandOption] = (
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
                    arguments[option.name] = self.convert_command_option_value(
                        interaction, option
                    )
        try:
            command: Command = self.workflow_manager.get_command(
                group_name, subgroup_name, command_name
            )
        except KeyError:
            raise Exception(
                f"Cannot access command with name {group_name} {subgroup_name} {command_name}"
            )
        try:
            context = await self.create_interaction_context(interaction, command)
            if command.is_defer:
                await context.defer()
            try:
                await command.callback(
                    command._workflow,
                    context,
                    **arguments,
                )
            except Exception as exception:
                await self.proceed_exception(context, exception)
        except Exception as exception:
            self.__logger.error(
                "error occurred while executing command %s %s %s.",
                group_name,
                subgroup_name,
                command_name,
                exc_info=exception,
            )
