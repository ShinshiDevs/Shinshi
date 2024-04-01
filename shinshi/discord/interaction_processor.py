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
from hikari.commands import CommandType
from hikari.events import InteractionCreateEvent
from hikari.interactions.base_interactions import PartialInteraction
from hikari.interactions.command_interactions import CommandInteraction
from hikari.locales import Locale

from shinshi.discord.bot import BaseBot
from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.processors import SlashCommandProcessor
from shinshi.discord.workflows.interactables.interactable import Interactable
from shinshi.discord.workflows.workflow_manager import WorkflowManager
from shinshi.i18n import I18nProvider

_DEFAULT_LANGUAGE: str = Locale.EN_US


class InteractionProcessor(SlashCommandProcessor):
    def __init__(
        self,
        bot: BaseBot,
        i18n_provider: I18nProvider,
        workflow_manager: WorkflowManager,
    ) -> None:
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
                    str(
                        interaction.locale
                        or interaction.guild_locale
                        or _DEFAULT_LANGUAGE
                    )
                )
            ),
            interactable=interactable,
        )

    async def proceed(self, event: InteractionCreateEvent) -> None:
        interaction: PartialInteraction = event.interaction
        if isinstance(interaction, CommandInteraction):
            if interaction.command_type is CommandType.SLASH:
                await self.proceed_slash_command(interaction)

    def install(self) -> None:
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.proceed)
