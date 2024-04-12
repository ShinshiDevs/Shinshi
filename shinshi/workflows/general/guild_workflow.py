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

from shinshi.discord.interactables.group import Group
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.utils.string import format_datetime


class GuildWorkflow(Workflow):
    GROUP = Group(name="guild")

    @staticmethod
    async def get_base_embed(context: InteractionContext, guild: GatewayGuild) -> Embed:
        embed = Embed(title=guild.name)
        if invites := await context.bot.rest.fetch_guild_invites(guild):
            embed.url = f"https://discord.gg/{invites[-1].code}"
        return embed

    @command(
        group=GROUP,
        name="info",
        description=Translatable("commands.guild.info.description"),
    )
    async def guild_info(self, context: InteractionContext) -> None:
        guild: GatewayGuild = context.interaction.get_guild()
        embed: Embed = (
            (await self.get_base_embed(context, guild))
            .set_thumbnail(guild.icon_url)
            .set_author(name=context.i18n.get("commands.guild.info.embed.author.name"))
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
                value=guild.member_count,
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.guild.info.embed.fields.channels.name"),
                value=len(guild.get_channels()),
                inline=True,
            )
        )
        return await context.create_response(embed=embed)
