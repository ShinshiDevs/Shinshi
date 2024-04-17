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
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from hikari.api import ComponentBuilder
from hikari.embeds import Embed
from hikari.files import Resourceish
from hikari.guilds import PartialRole
from hikari.interactions import CommandInteraction, ComponentInteraction, ResponseType
from hikari.messages import Message, MessageFlag
from hikari.snowflakes import SnowflakeishSequence
from hikari.undefined import UNDEFINED, UndefinedOr
from hikari.users import PartialUser

from shinshi.discord.bot import Bot
from shinshi.discord.interactables.interactable import Interactable
from shinshi.i18n import I18nGroup

type InteractionT = CommandInteraction | ComponentInteraction
# TODO: Remove this, emojis.json must be used
ERROR_EMOJI: tuple[str, int] = "exclamation", 1228757404666171402
WARNING_EMOJI: tuple[str, int] = "warning", 1228757406029189230


@dataclass(kw_only=True)
class InteractionContext:
    interaction: InteractionT
    bot: Bot
    i18n: I18nGroup
    interactable: Interactable

    _has_created_response: bool = False
    _has_deferred_response: bool = False

    async def defer(self) -> None:
        await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            token=self.interaction.token,
            flags=(
                MessageFlag.EPHEMERAL if self.interactable.is_ephemeral else UNDEFINED
            ),
            response_type=ResponseType.DEFERRED_MESSAGE_CREATE,
        )
        self._has_deferred_response = True

    async def create_response(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        flags: UndefinedOr[MessageFlag] = UNDEFINED,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
        mentions_everyone: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[
            SnowflakeishSequence[PartialUser] | bool
        ] = UNDEFINED,
        role_mentions: UndefinedOr[
            SnowflakeishSequence[PartialRole] | bool
        ] = UNDEFINED,
        ensure_message: bool = False,
    ) -> Message | None:
        kwargs: dict[str, Any] = dict(
            token=self.interaction.token,
            content=content,
            attachment=attachment,
            attachments=attachments,
            component=component,
            components=components,
            embed=embed,
            embeds=embeds,
            mentions_everyone=mentions_everyone,
            user_mentions=user_mentions,
            role_mentions=role_mentions,
        )
        if self._has_deferred_response:
            await self.bot.rest.edit_interaction_response(
                application=self.interaction.application_id,
                **kwargs,
            )
        else:
            await self.bot.rest.create_interaction_response(
                interaction=self.interaction.id,
                response_type=ResponseType.MESSAGE_CREATE,
                flags=flags,
                **kwargs,
            )
        if ensure_message:
            return await self.bot.rest.fetch_interaction_response(
                self.interaction.id, self.interaction.token
            )

    async def edit_response(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
    ) -> Message | None:
        return await self.bot.rest.edit_interaction_response(
            application=self.interaction.application_id,
            token=self.interaction.token,
            content=content,
            attachment=attachment,
            attachments=attachments,
            component=component,
            components=components,
            embed=embed,
            embeds=embeds,
        )

    async def delete_response(self) -> None:
        await self.bot.rest.delete_interaction_response(
            application=self.interaction.application_id, token=self.interaction.token
        )

    async def send_error(self, content: UndefinedOr[Any] = UNDEFINED) -> None:
        return await self.create_response(
            content=" ".join((f"<:{ERROR_EMOJI[0]}:{ERROR_EMOJI[1]}>", content)),
            flags=MessageFlag.EPHEMERAL,
        )

    async def send_warning(self, content: UndefinedOr[Any] = UNDEFINED) -> None:
        return await self.create_response(
            content=" ".join((f"<:{WARNING_EMOJI[0]}:{WARNING_EMOJI[1]}>", content)),
            flags=MessageFlag.EPHEMERAL,
        )
