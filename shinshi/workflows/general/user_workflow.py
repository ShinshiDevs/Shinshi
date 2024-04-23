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
from datetime import timedelta

from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.guilds import Role
from hikari.impl import (
    LinkButtonBuilder,
    MessageActionRowBuilder,
)
from hikari.interactions import InteractionMember
from hikari.users import User, UserFlag

from shinshi import IMAGES_DIR
from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.options import Option
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.ext.colour import Colour
from shinshi.ext.hooks.cooldown import Cooldown
from shinshi.utils.string import format_datetime


class UserWorkflow(Workflow):
    GROUP = Group(name="user", is_dm_enabled=True)
    OPTIONS: list[Option] = [
        Option(
            type=OptionType.USER,
            name="target",
            description=Translatable("commands.user.arguments.target.description"),
            is_required=False,
        )
    ]

    @command(
        group=GROUP,
        name="info",
        description=Translatable("commands.user.info.description"),
        options=OPTIONS,
    )
    async def user_info(
        self,
        context: InteractionContext,
        target: InteractionMember | User | None = None,
    ) -> None:
        user: InteractionMember | User = target or context.interaction.member  # type: ignore
        icon_name: str = (
            "user"
            if not user.is_bot
            else f"{"verified_" if UserFlag.VERIFIED_BOT in user.flags else ""}bot"
        ) + ".webp"
        embed = (
            Embed(
                title=user.global_name or user.username,
                url=f"https://discordapp.com/users/{user.id}",
                description=f"@{user.username}" if user.global_name else None,
                colour=Colour.DARK,
            )
            .set_thumbnail(user.display_avatar_url)
            .set_author(
                name=context.i18n.get("commands.user.info.embed.author.name"),
                icon=IMAGES_DIR / icon_name,
            )
            .set_footer(text=f"ID: {user.id}")
            .add_field(
                name=context.i18n.get(
                    "commands.user.info.embed.fields.created_at.name"
                ),
                value=(
                    f"{format_datetime(user.created_at, "R")}\n"
                    f"{format_datetime(user.created_at, "D")}"
                ),
                inline=True,
            )
        )
        if isinstance(user, InteractionMember):
            roles: list[Role] = sorted(
                user.get_roles(), key=lambda role: role.position, reverse=True
            )
            embed.add_field(
                name=context.i18n.get(
                    "commands.user.info.embed.fields.joined_at.name",
                    {"guild": user.get_guild().name},  # type: ignore  # InteractionMember always has a guild
                ),
                value=(
                    f"{format_datetime(user.joined_at, "R")}\n"  # type: ignore  # the same... mypy is stupid
                    f"{format_datetime(user.joined_at, "D")}"  # type: ignore
                ),
                inline=True,
            )
            embed.title = user.display_name
            if colour := next((role.colour for role in roles if role.colour), None):
                embed.colour = colour
            if roles := [role.mention for role in roles if role.id != user.guild_id]:  # type: ignore
                if len(roles) > 5:
                    embed.add_field(
                        name=context.i18n.get(
                            "commands.user.info.embed.fields.roles.name"
                        ),
                        value=context.i18n.get(
                            "commands.user.info.embed.fields.roles.value.many_roles",
                            {
                                "roles": ", ".join(roles[:5]),  # type: ignore
                                "count": int(len(roles) - 5),
                            },
                        ),
                    )
                else:
                    embed.add_field(
                        name=context.i18n.get(
                            "commands.user.info.embed.fields.roles.name"
                        ),
                        value=", ".join(roles),
                    )
            else:
                embed.add_field(
                    name=context.i18n.get("commands.user.info.embed.fields.roles.name"),
                    value=context.i18n.get(
                        "commands.user.info.embed.fields.roles.value.no_roles"
                    ),
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
        target: InteractionMember | User | None = None,
    ) -> None:
        user: InteractionMember | User = target or context.interaction.member  # type: ignore
        if user.avatar_url is None:
            return await context.send_warning(
                context.i18n.get(
                    "commands.user.avatar.exceptions.no_avatar_exception",
                    {
                        "user": user.username or user.global_name,
                    },
                )
            )
        return await context.create_response(
            embed=(
                Embed(colour=Colour.DARK)
                .set_image(user.avatar_url)
                .set_author(
                    name=context.i18n.get(
                        "commands.user.avatar.embed.author.name",
                        {"user": user.global_name or user.username},
                    )
                )
            ),
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=f"{res}x{res}",
                        url=target.make_avatar_url(size=res).url,  # type: ignore
                    )
                    for res in (256, 512, 1024)
                ]
            ),
        )

    @command(
        group=GROUP,
        name="banner",
        description=Translatable("commands.user.banner.description"),
        options=OPTIONS,
        hooks=[Cooldown(period=timedelta(seconds=5)).hook],
    )
    async def user_banner(
        self,
        context: InteractionContext,
        target: InteractionMember | User | None = None,
    ) -> None:
        target = await context.bot.rest.fetch_user(target or context.interaction.user)
        if target.banner_url is None:
            return await context.send_warning(
                context.i18n.get(
                    "commands.user.banner.exceptions.no_banner_exception",
                    {
                        "user": target.username or target.global_name,
                    },
                )
            )
        return await context.create_response(
            embed=(
                Embed(colour=Colour.DARK)
                .set_image(target.banner_url)
                .set_author(
                    name=context.i18n.get(
                        "commands.user.banner.embed.author.name",
                        {"user": target.global_name or target.username},
                    ),
                    icon=target.display_avatar_url,
                )
            ),
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=context.i18n.get("buttons.open.label"),
                        url=target.banner_url.url,
                    )
                ]
            ),
        )
