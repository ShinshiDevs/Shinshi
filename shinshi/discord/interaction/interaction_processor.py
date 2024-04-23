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
from typing import Any

from hikari import errors
from hikari.commands import CommandType, OptionType
from hikari.events import InteractionCreateEvent
from hikari.interactions import (
    CommandInteraction,
    CommandInteractionOption,
    ComponentInteraction,
    PartialInteraction,
)
from sentry_sdk import capture_exception

from shinshi import IMAGES_DIR
from shinshi.discord.bot import Bot
from shinshi.discord.constants import DEFAULT_LANGUAGE
from shinshi.discord.interactables.hooks.hook_result import HookResult
from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.discord.interaction.utils import get_interaction_argument
from shinshi.discord.workflows import WorkflowManager
from shinshi.discord.workflows.constants import INTERACTABLE_WORKFLOW_INSTANCE
from shinshi.i18n import I18nProvider


class InteractionProcessor:
    __slots__: tuple[str, ...] = (
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
        self.bot = bot
        self.bot.event_manager.subscribe(
            InteractionCreateEvent, self.proceed_interaction
        )

        self.i18n_provider = i18n_provider
        self.workflow_manager = workflow_manager

    async def proceed_interaction(self, event: InteractionCreateEvent) -> None:
        if isinstance(event.interaction, CommandInteraction):
            if event.interaction.command_type == CommandType.SLASH:
                await self.proceed_slash_command(event.interaction)

    async def proceed_slash_command(self, interaction: CommandInteraction) -> None:
        group_name, subgroup_name = None, None
        command_name = interaction.command_name
        arguments: dict[str, Any] = {}
        options: list[CommandInteractionOption] = list(interaction.options or [])
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
                    arguments[option.name] = get_interaction_argument(
                        interaction, option
                    )
        command = self.workflow_manager.get_command(
            group_name, subgroup_name, command_name
        )
        if not command:
            raise ValueError(
                f"Cannot access command {group_name} {subgroup_name} {command_name}"
            )
        context = self.create_interaction_context(interaction, command)
        context.arguments = arguments
        try:
            for hook in command.hooks:
                result: HookResult = await hook.callback(context)  # type: ignore
                if result.stop:
                    return
            await command.callback(
                getattr(command, INTERACTABLE_WORKFLOW_INSTANCE),
                context,
                **arguments,
            )
        except Exception as exception:
            await self.proceed_exception(context, exception)

    def create_interaction_context(
        self,
        interaction: PartialInteraction,
        interactable: Interactable,
    ) -> InteractionContext:
        if not isinstance(interaction, (CommandInteraction, ComponentInteraction)):
            raise ValueError("Not valid interaction type")
        return InteractionContext(
            interaction=interaction,
            bot=self.bot,
            i18n=(
                self.i18n_provider.languages.get(
                    str(interaction.locale or interaction.guild_locale),
                    self.i18n_provider.languages[DEFAULT_LANGUAGE],
                )
            ),
            interactable=interactable,
        )

    async def proceed_exception(
        self, context: InteractionContext, exception: Exception
    ) -> None:
        exception = getattr(exception, "original", exception)
        if isinstance(exception, errors.NotFoundError):
            await context.send_warning(
                context.i18n.get("errors.hikari.not_found_error")
            )
            return
        elif isinstance(exception, errors.ForbiddenError):
            await context.send_error(context.i18n.get("errors.hikari.forbidden"))
            return
        elif isinstance(exception, errors.RateLimitTooLongError):
            await context.send_error(
                content=context.i18n.get("errors.hikari.ratelimit"),
                icon=IMAGES_DIR / "ratelimit.webp",
            )
            return
        capture_exception(exception)
        await context.send_error(
            content=context.i18n.get("exceptions.unknown_exception.content"),
            description=context.i18n.get("exceptions.unknown_exception.description"),
        )
