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
from typing import Sequence

from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.guilds import Member, Role
from hikari.interactions import InteractionMember
from hikari.users import User, UserFlag

from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import WorkflowBase
from shinshi.discord.workflows.decorators import sub_command
from shinshi.discord.workflows.interactables.group import Group
from shinshi.discord.workflows.interactables.options import Option
from shinshi.i18n import I18nGroup
from shinshi.utils.datetime import format_datetime
from shinshi.utils.icons import get_icon


class UserWorkflow(WorkflowBase):
    GROUP = Group(name="user", is_dm_enabled=True)
    OPTIONS = (
        Option(
            type=OptionType.USER,
            name="target",
            description=Translatable("commands.user.arguments.target.description"),
            is_required=False,
        ),
    )

    @staticmethod
    def __unwrap_target(
        context: InteractionContext, target: User | InteractionMember | None
    ) -> User | InteractionMember:
        user: User | InteractionMember
        if not target:
            user = context.interaction.user or context.interaction.member
        else:
            user = target
        return user

    @staticmethod
    def __add_roles_field(
        context: InteractionContext, embed: Embed, user: Member | InteractionMember
    ) -> None:
        i18n: I18nGroup = context.i18n
        sorted_roles: Sequence[Role] = sorted(
            user.get_roles(), key=lambda role: role.position, reverse=True
        )
        roles: Sequence[str] = [
            role.mention for role in sorted_roles if role.id != user.guild_id
        ]
        if not roles:
            embed.add_field(
                name=i18n.get("commands.user.info.embed.fields.roles.name"),
                value=i18n.get("commands.user.info.embed.fields.roles.value.no_roles"),
                inline=False,
            )
        else:
            if len(roles) > 5:
                embed.add_field(
                    name=i18n.get("commands.user.info.embed.fields.roles.name"),
                    value=i18n.get(
                        "commands.user.info.embed.fields.roles.value.many_roles",
                        {"roles": ", ".join(roles[:5]), "count": int(len(roles) - 5)},
                    ),
                    inline=False,
                )
            else:
                embed.add_field(
                    name=i18n.get("commands.user.info.embed.fields.roles.name"),
                    value=", ".join(roles),
                    inline=False,
                )

    @sub_command(
        group=GROUP,
        name="info",
        description=Translatable("commands.user.info.description"),
        options=OPTIONS,
    )
    async def user_info(
        self,
        context: InteractionContext,
        target: User | InteractionMember | None = None,
    ) -> None:
        target: User | InteractionMember = target or context.interaction.member
        i18n: I18nGroup = context.i18n
        embed = (
            Embed(
                title=getattr(target, "display_name", target.global_name)
                or target.username,
                url=f"https://discordapp.com/users/{target.id}",
                description=(
                    f"@{target.username}"
                    if not target.global_name
                    or not getattr(target, "display_name", None)
                    else None
                ),
            )
            .set_thumbnail(
                getattr(target, "guild_avatar_url", None) or target.display_avatar_url
            )
            .set_author(
                name=i18n.get("commands.user.info.embed.author.name"),
                icon=(
                    get_icon("user")
                    if not target.is_bot
                    else get_icon(
                        "bot"
                        if UserFlag.VERIFIED_BOT not in target.flags
                        else "bot_verified"
                    )
                ),
            )
            .set_footer(text=f"ID: {target.id}")
            .add_field(
                name=i18n.get("commands.user.info.embed.fields.created_at.name"),
                value=f"{format_datetime(target.created_at, 'R')}\n"
                f"{format_datetime(target.created_at, 'D')}",
                inline=True,
            )
        )

        if isinstance(target, Member):
            embed.color = getattr(target.get_top_role(), "color", None)
            embed.add_field(
                name=i18n.get(
                    "commands.user.info.embed.fields.joined_at.name",
                    {"guild": target.get_guild().name},
                ),
                value=f"{format_datetime(target.joined_at, 'R')}\n"
                f"{format_datetime(target.joined_at, 'D')}",
                inline=True,
            )
            self.__add_roles_field(context, embed, target)

        return await context.create_response(embed=embed)

    @sub_command(
        group=GROUP,
        name="avatar",
        description=Translatable("commands.user.avatar.description"),
        options=OPTIONS,
    )
    async def user_avatar(
        self, context: InteractionContext, target: Member | User | None = None
    ) -> None:
        i18n: I18nGroup = context.i18n
        user: User | Member | InteractionMember = self.__unwrap_target(context, target)
        if user.avatar_url is None:
            raise Exception(context)
        embed = (
            Embed(
                title=(
                    user.global_name
                    or (
                        user.display_name
                        if isinstance(user, Member | InteractionMember)
                        else None
                    )
                    or user.username
                ),
                url=f"https://discordapp.com/users/{user.id}",
                description=" ".join(
                    [
                        f"[`[{resolution}]`]({user.make_avatar_url(size=resolution).url})"
                        for resolution in (256, 512, 1024)
                    ]
                ),
            )
            .set_image(user.avatar_url or user.display_avatar_url)
            .set_author(name=i18n.get("commands.user.avatar.embed.author.name"))
        )
        return await context.create_response(embed=embed)

    @sub_command(
        group=GROUP,
        name="banner",
        description=Translatable("commands.user.banner.description"),
        options=OPTIONS,
    )
    async def user_banner(
        self, context: InteractionContext, target: Member | User | None = None
    ) -> None:
        i18n: I18nGroup = context.i18n
        user: User = await self.__unwrap_target(context, target).fetch_self()
        if user.banner_url is None:
            raise Exception(context)
        return await context.create_response(
            embed=(
                Embed(
                    title=user.global_name or user.username,
                    url=f"https://discordapp.com/users/{user.id}",
                    description=" ".join(
                        [
                            f"[`[{resolution}]`]({user.make_banner_url(size=resolution).url})"
                            for resolution in (256, 512, 1024)
                        ]
                    ),
                )
                .set_image(user.banner_url)
                .set_author(
                    name=i18n.get("commands.user.banner.embed.author.name"),
                    icon=user.display_avatar_url,
                )
            )
        )
