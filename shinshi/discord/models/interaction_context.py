from dataclasses import dataclass
from typing import Any, Sequence, Tuple, Dict

from hikari import Locale
from hikari.api import ComponentBuilder
from hikari.embeds import Embed
from hikari.files import Resourceish
from hikari.guilds import PartialRole, PartialGuild
from hikari.interactions import CommandInteraction, ComponentInteraction, ResponseType
from hikari.messages import Message
from hikari.messages import MessageFlag
from hikari.snowflakes import SnowflakeishSequence
from hikari.undefined import UNDEFINED, UndefinedOr
from hikari.users import PartialUser

from shinshi.discord.bot import Bot
from shinshi.discord.enum.translation_type import TranslationType
from shinshi.discord.interactables.interactable import Interactable
from shinshi.i18n import I18nProvider


@dataclass(kw_only=True)
class InteractionContext:
    bot: Bot
    i18n_provider: I18nProvider
    interaction: CommandInteraction | ComponentInteraction

    interactable: Interactable

    _has_created_response: bool = False
    _has_deferred_response: bool = False

    async def defer(self) -> None:
        await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            token=self.interaction.token,
            flags=MessageFlag.EPHEMERAL if self.interactable.is_ephemeral else UNDEFINED,
            response_type=ResponseType.DEFERRED_MESSAGE_CREATE,
        )
        self._has_deferred_response = True

    async def create_response(
        self,
        content: UndefinedOr[Any] = UNDEFINED,
        *,
        attachment: UndefinedOr[Resourceish] = UNDEFINED,
        attachments: UndefinedOr[Sequence[Resourceish]] = UNDEFINED,
        component: UndefinedOr[ComponentBuilder] = UNDEFINED,
        components: UndefinedOr[Sequence[ComponentBuilder]] = UNDEFINED,
        embed: UndefinedOr[Embed] = UNDEFINED,
        embeds: UndefinedOr[Sequence[Embed]] = UNDEFINED,
        mentions_everyone: UndefinedOr[bool] = UNDEFINED,
        user_mentions: UndefinedOr[SnowflakeishSequence[PartialUser] | bool] = UNDEFINED,
        role_mentions: UndefinedOr[SnowflakeishSequence[PartialRole] | bool] = UNDEFINED,
        ensure_message: bool = False,
    ) -> Message | None:
        response_type: ResponseType = ResponseType.MESSAGE_CREATE
        if self._has_deferred_response:
            response_type = ResponseType.DEFERRED_MESSAGE_UPDATE
        else:
            if self.interactable.defer:
                await self.defer()
        await self.bot.rest.create_interaction_response(
            interaction=self.interaction.id,
            token=self.interaction.token,
            response_type=response_type,
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

    def get_guild(self) -> PartialGuild:
        return self.interaction.get_guild()

    def translate(
        self,
        key: str,
        arguments: Dict[str, Any] | None = None,
        *,
        translation_type: TranslationType = TranslationType.TEXT,
    ) -> str | Tuple[str, ...] | None:
        locale: Locale = self.interaction.locale or self.interaction.guild_locale
        match translation_type:
            case TranslationType.TEXT:
                return self.i18n_provider.get(key, arguments, locale=locale)
            case TranslationType.LIST:
                return self.i18n_provider.get_list(key, locale=locale)
