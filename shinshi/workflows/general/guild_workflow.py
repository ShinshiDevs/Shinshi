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
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild
from hikari.impl import LinkButtonBuilder, MessageActionRowBuilder

from shinshi import IMAGES_DIR
from shinshi.discord.interactables.group import Group
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.ext.colour import Colour
from shinshi.utils.string import format_datetime


class GuildWorkflow(Workflow):
    GROUP = Group(name="guild")

    @command(
        group=GROUP,
        name="info",
        description=Translatable("commands.guild.info.description"),
    )
    async def guild_info(self, context: InteractionContext) -> None:
        guild: GatewayGuild = context.interaction.get_guild()
        embed = (
            Embed(title=guild.name, colour=Colour.DARK)
            .set_thumbnail(guild.icon_url)
            .set_author(
                name=context.i18n.get("commands.guild.info.embed.author.name"),
                icon=IMAGES_DIR / "guild.webp",
            )
            .set_footer(text=f"ID: {guild.id}")
            .add_field(
                name=context.i18n.get("commands.guild.info.embed.fields.owner.name"),
                value=f"<@!{guild.owner_id}>",
                inline=True,
            )
            .add_field(
                name=context.i18n.get(
                    "commands.guild.info.embed.fields.created_at.name"
                ),
                value=(
                    f"{format_datetime(guild.created_at, "R")}\n"
                    f"{format_datetime(guild.created_at, "D")}"
                ),
                inline=True,
            )
            .add_field(
                name=context.i18n.get(
                    "commands.guild.info.embed.fields.you_joined_at.name"
                ),
                value=(
                    f"{format_datetime(context.interaction.member.joined_at, "R")}\n"
                    f"{format_datetime(context.interaction.member.joined_at, "D")}"
                ),
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.guild.info.embed.fields.members.name"),
                value=str(guild.member_count),
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.guild.info.embed.fields.channels.name"),
                value=str(len(guild.get_channels())),
                inline=True,
            )
        )
        return await context.create_response(embed=embed)

    @command(
        group=GROUP,
        name="icon",
        description=Translatable("commands.guild.icon.description"),
    )
    async def guild_icon(self, context: InteractionContext) -> None:
        guild: GatewayGuild = context.interaction.get_guild()
        if guild.icon_url is None:
            return await context.send_warning(
                context.i18n.get(
                    "commands.guild.icon.exceptions.no_icon_exception",
                )
            )
        return await context.create_response(
            embed=(
                Embed(colour=Colour.DARK)
                .set_image(guild.icon_url)
                .set_author(
                    name=context.i18n.get(
                        "commands.guild.icon.embed.author.name",
                        {"guild": guild.name},
                    )
                )
            ),
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=f"{res}x{res}",
                        url=guild.make_icon_url(size=res).url,
                    )
                    for res in (256, 512, 1024)
                ]
            ),
        )

    @command(
        group=GROUP,
        name="splash",
        description=Translatable("commands.guild.splash.description"),
    )
    async def guild_splash(self, context: InteractionContext) -> None:
        guild: GatewayGuild = context.interaction.get_guild()
        if not guild.splash_url:
            return await context.send_warning(
                context.i18n.get(
                    "commands.guild.splash.exceptions.no_splash_exception",
                )
            )
        return await context.create_response(
            embed=(
                Embed(colour=Colour.DARK)
                .set_image(guild.splash_url)
                .set_author(
                    name=context.i18n.get(
                        "commands.guild.splash.embed.author.name", {"guild": guild.name}
                    )
                )
            ),
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=context.i18n.get("buttons.open.label"),
                        url=guild.splash_url.url,
                    )
                ]
            ),
        )

    @command(
        group=GROUP,
        name="banner",
        description=Translatable("commands.guild.banner.description"),
    )
    async def guild_banner(self, context: InteractionContext) -> None:
        guild: GatewayGuild = context.interaction.get_guild()
        if not guild.banner_url:
            return await context.send_warning(
                context.i18n.get(
                    "commands.guild.banner.exceptions.no_banner_exception",
                )
            )
        return await context.create_response(
            embed=(
                Embed(colour=Colour.DARK)
                .set_image(guild.banner_url)
                .set_author(
                    name=context.i18n.get(
                        "commands.guild.banner.embed.author.name", {"guild": guild.name}
                    )
                )
            ),
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=context.i18n.get("buttons.open.label"),
                        url=guild.banner_url.url,
                    )
                ]
            ),
        )
