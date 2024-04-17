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
import logging
from typing import Any

from hikari.commands import CommandOption, CommandType, OptionType
from hikari.events import InteractionCreateEvent
from hikari.guilds import Role
from hikari.interactions import (
    CommandInteraction,
    InteractionChannel,
    InteractionMember,
    PartialInteraction,
)
from hikari.users import User
from sentry_sdk import capture_exception, push_scope

from shinshi.discord.bot import Bot
from shinshi.discord.constants import DEFAULT_LANGUAGE
from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.hooks import HookResult
from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.discord.interaction.interaction_exception import InteractionException
from shinshi.discord.workflows import WorkflowManager
from shinshi.discord.workflows.constants import INTERACTABLE_WORKFLOW_INSTANCE
from shinshi.i18n import I18nProvider

type ValueT = (
    User | InteractionMember | InteractionChannel | Role | str | int | float | None
)


class InteractionProcessor:
    __slots__: tuple[str, ...] = (
        "__logger",
        "bot",
        "i18n_provider",
        "workflow_manager",
    )

    def __init__(
        self,
        bot: Bot,
        i18n_provider: I18nProvider,
        workflow_manager: WorkflowManager,
    ) -> None:
        self.__logger = logging.getLogger("shinshi.interactions")

        self.bot = bot
        self.i18n_provider = i18n_provider
        self.workflow_manager = workflow_manager

    async def create_interaction_context(
        self, interaction: PartialInteraction, interactable: Interactable
    ) -> InteractionContext:
        return InteractionContext(
            interaction=interaction,
            bot=self.bot,
            i18n=(
                self.i18n_provider.languages.get(
                    interaction.locale or interaction.guild_locale,
                    self.i18n_provider.languages[DEFAULT_LANGUAGE],
                )
            ),
            interactable=interactable,
        )

    def convert_command_option_value(
        self, interaction: CommandInteraction, option: CommandOption
    ) -> ValueT:
        match option.type:
            case OptionType.STRING:
                return str(option.value)
            case OptionType.INTEGER:
                return int(option.value)
            case OptionType.BOOLEAN:
                return bool(option.value)
            case OptionType.USER:
                return interaction.resolved.members.get(
                    option.value
                ) or interaction.resolved.users.get(option.value)
            case OptionType.CHANNEL:
                return interaction.resolved.channels.get(option.value)
            case OptionType.ROLE:
                return interaction.resolved.roles.get(option.value)
            case OptionType.MENTIONABLE:
                return interaction.resolved.members.get(
                    option.value
                ) or interaction.resolved.roles.get(option.value)
            case OptionType.FLOAT:
                return float(option.value)
            case OptionType.ATTACHMENT:
                return interaction.resolved.attachments.get(option.value)
            case _:
                return

    async def proceed_interaction(self, event: InteractionCreateEvent) -> None:
        if isinstance(event.interaction, CommandInteraction):
            match event.interaction.command_type:
                case CommandType.SLASH:
                    await self.proceed_slash_command(event.interaction)

    async def proceed_exception(
        self, context: InteractionContext, exception: Exception
    ) -> None:
        if isinstance(exception, InteractionException):
            return await exception.callback()
        with push_scope() as scope:
            if isinstance(context.interactable, Command):
                scope.set_tag("command", context.interactable.qualname)
            scope.set_tag("user ID", context.interaction.user.id)
            scope.level = "warning"
            capture_exception(exception)
        return await context.send_error(
            context.i18n.get("exceptions.unknown_exception")
        )

    async def proceed_slash_command(self, interaction: CommandInteraction) -> None:
        group_name, subgroup_name, command_name = None, None, interaction.command_name
        arguments: dict[str, Any] = {}
        options: list[CommandOption] = interaction.options or []
        for option in options:
            if option.type == OptionType.SUB_COMMAND_GROUP:
                group_name = interaction.command_name
                subgroup_name = option.name
            elif option.type == OptionType.SUB_COMMAND:
                group_name = group_name or interaction.command_name
                command_name = option.name
            else:
                arguments[option.name] = self.convert_command_option_value(
                    interaction, option
                )
        if command := self.workflow_manager.get_command(
            group_name, subgroup_name, command_name
        ):
            context = await self.create_interaction_context(interaction, command)
            try:
                if command.is_defer:
                    await context.defer()
                for hook in command.hooks:
                    result: HookResult = await hook()
                    if result.stop:
                        return
                await command.callback(
                    getattr(command, INTERACTABLE_WORKFLOW_INSTANCE),
                    context,
                    **arguments,
                )
            except Exception as exception:
                await self.proceed_exception(context, exception)
        else:
            self.__logger.error(
                "Cannot access %s command",
                f"{group_name} {subgroup_name} {command}".replace("None", ""),
            )
