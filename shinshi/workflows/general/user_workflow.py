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
from typing import Sequence, Tuple

from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.impl import (
    LinkButtonBuilder,
    MessageActionRowBuilder,
)
from hikari.interactions import InteractionMember
from hikari.users import User, UserFlag

from shinshi import IMAGES_DIR
from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.options import Option
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.utils.string import format_datetime
from shinshi.workflows.general.exceptions import (
    UserAvatarAvailabilityException,
    UserBannerAvailabilityException,
)


class UserWorkflow(Workflow):
    GROUP = Group(name="user", is_dm_enabled=True)
    OPTIONS: Tuple[Option, ...] = (
        Option(
            type=OptionType.USER,
            name="target",
            description=Translatable("commands.user.arguments.target.description"),
            is_required=False,
        ),
    )

    @staticmethod
    def __get_base_embed(target: User | InteractionMember):
        colour: int | None = None
        if isinstance(target, InteractionMember):
            colour = next(
                (role.colour for role in target.get_roles() if role.colour), None
            )
        title = (
            target.display_name
            if hasattr(target, "display_name")
            else target.global_name or target.username
        )
        return Embed(
            title=title,
            url=f"https://discordapp.com/users/{target.id}",
            description=f"@{target.username}" if title != target.username else None,
            colour=colour,
        )

    @command(
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
        icon_name = (
            "user"
            if not target.is_bot
            else f"bot{"_verified" if UserFlag.VERIFIED_BOT in target.flags else ""}"
        ) + ".webp"
        embed: Embed = (
            self.__get_base_embed(target)
            .set_thumbnail(target.display_avatar_url)
            .set_author(
                name=context.i18n.get("commands.user.info.embed.author.name"),
                icon=IMAGES_DIR / icon_name,
            )
            .set_footer(text=f"ID: {target.id}")
            .add_field(
                name=context.i18n.get(
                    "commands.user.info.embed.fields.created_at.name"
                ),
                value=(
                    f"{format_datetime(target.created_at, "R")}\n"
                    f"{format_datetime(target.created_at, "D")}"
                ),
                inline=True,
            )
        )
        if isinstance(target, InteractionMember):
            embed.add_field(
                name=context.i18n.get(
                    "commands.user.info.embed.fields.joined_at.name",
                    {"guild": target.get_guild().name},
                ),
                value=(
                    f"{format_datetime(target.joined_at, "R")}\n"
                    f"{format_datetime(target.joined_at, "D")}"
                ),
                inline=True,
            )
            roles: Sequence[str] = [
                role.mention
                for role in sorted(
                    target.get_roles(), key=lambda role: role.position, reverse=True
                )
                if role.id != target.guild_id
            ]
            if not roles:
                embed.add_field(
                    name=context.i18n.get("commands.user.info.embed.fields.roles.name"),
                    value=context.i18n.get(
                        "commands.user.info.embed.fields.roles.value.no_roles"
                    ),
                    inline=False,
                )
            else:
                if len(roles) > 5:
                    embed.add_field(
                        name=context.i18n.get(
                            "commands.user.info.embed.fields.roles.name"
                        ),
                        value=context.i18n.get(
                            "commands.user.info.embed.fields.roles.value.many_roles",
                            {
                                "roles": ", ".join(roles[:5]),
                                "count": int(len(roles) - 5),
                            },
                        ),
                        inline=False,
                    )
                else:
                    embed.add_field(
                        name=context.i18n.get(
                            "commands.user.info.embed.fields.roles.name"
                        ),
                        value=", ".join(roles),
                        inline=False,
                    )
        return await context.create_response(embed=embed)

    @command(
        group=GROUP,
        name="avatar",
        description=Translatable("commands.user.avatar.description"),
        options=OPTIONS,
    )
    async def user_avatar(
        self,
        context: InteractionContext,
        target: User | InteractionMember | None = None,
    ) -> None:
        target: User | InteractionMember = target or context.interaction.member
        if target.avatar_url is None:
            raise UserAvatarAvailabilityException(context, target)
        embed: Embed = (
            self.__get_base_embed(target)
            .set_image(target.avatar_url)
            .set_author(name=context.i18n.get("commands.user.avatar.embed.author.name"))
        )
        return await context.create_response(
            embed=embed,
            component=MessageActionRowBuilder(
                components=(
                    LinkButtonBuilder(
                        label=f"{res}x{res}", url=target.make_avatar_url(size=res).url
                    )
                    for res in (256, 512, 1024)
                )
            ),
        )

    @command(
        group=GROUP,
        name="banner",
        description=Translatable("commands.user.banner.description"),
        options=OPTIONS,
    )
    async def user_banner(
        self,
        context: InteractionContext,
        target: User | InteractionMember | None = None,
    ) -> None:
        target: User = await (target or context.interaction.user).fetch_self()
        if target.banner_url is None:
            raise UserBannerAvailabilityException(context, target)
        return await context.create_response(
            embed=(
                self.__get_base_embed(target)
                .set_image(target.banner_url)
                .set_author(
                    name=context.i18n.get("commands.user.banner.embed.author.name"),
                    icon=target.display_avatar_url,
                    url=target.banner_url.url,
                )
            ),
        )
