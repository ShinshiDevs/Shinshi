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

from hikari import Role
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.impl import (
    LinkButtonBuilder,
    MessageActionRowBuilder,
)
from hikari.interactions import InteractionMember
from hikari.users import User, UserFlag

from shinshi import IMAGES_DIR
from shinshi.discord.ext.hooks.cooldown import cooldown
from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.options import Option
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.utils.string import format_datetime
from shinshi.workflows.general.exceptions import (
    NoUserAvatarException,
    NoUserBannerException,
)

type TargetT = InteractionMember | User | None


class UserWorkflow(Workflow):
    GROUP = Group(name="user", is_dm_enabled=True)
    OPTIONS: tuple[Option, ...] = (
        Option(
            type=OptionType.USER,
            name="target",
            description=Translatable("commands.user.arguments.target.description"),
            is_required=False,
        ),
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
        target: TargetT = None,
    ) -> None:
        target = target or context.interaction.member
        icon_name: str = (
            "user"
            if not target.is_bot
            else f"bot{"_verified" if UserFlag.VERIFIED_BOT in target.flags else ""}"
        ) + ".webp"
        embed = (
            Embed(
                title=target.global_name or target.username,
                url=f"https://discordapp.com/users/{target.id}",
                description=f"@{target.username}" if not target.global_name else None,
            )
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
            roles: list[Role] = sorted(
                target.get_roles(), key=lambda role: role.position, reverse=True
            )
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
            embed.title = target.display_name
            embed.colour = next((role.colour for role in roles if role.colour), None)
            if roles := tuple[str](
                role.mention for role in roles if role.id != target.guild_id
            ):
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
        target: TargetT = None,
    ) -> None:
        target = target or context.interaction.member
        if target.avatar_url is None:
            raise NoUserAvatarException(context, target)
        return await context.create_response(
            embed=(
                Embed()
                .set_image(target.avatar_url)
                .set_author(
                    name=context.i18n.get(
                        "commands.user.avatar.embed.author.name",
                        {"user": target.global_name or target.username},
                    )
                )
            ),
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
        hooks=[cooldown(period=timedelta(seconds=5))],
    )
    async def user_banner(
        self,
        context: InteractionContext,
        target: TargetT = None,
    ) -> None:
        target = await context.bot.rest.fetch_user(target or context.interaction.user)
        if target.banner_url is None:
            raise NoUserBannerException(context, target)
        return (
            await context.create_response(
                embed=(
                    Embed()
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
            ),
        )
