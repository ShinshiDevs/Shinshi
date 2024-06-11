# Shinshi - A modern and user-friendly Discord bot designed to give you and your servers great functionality and stable performance.
# Copyright (C) 2024 Shinshi Developers Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from collections.abc import Sequence

from aurum.commands import SlashCommand
from aurum.commands.decorators import sub_command
from aurum.interactions import InteractionContext
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild

from shinshi import __version__
from shinshi.colour import Colour
from shinshi.utils.datetime import format_datetime


class AboutCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("about")

    @sub_command("bot")
    async def about_bot(self, context: InteractionContext) -> None:
        guilds: Sequence[GatewayGuild] = tuple(
            context.bot.cache.get_guilds_view().values()
        )
        members_count: int = sum(guild.member_count for guild in guilds)  # type: ignore
        return await context.create_response(
            embed=(
                Embed(
                    title="Shinshi",
                    description="A modern and user-friendly Discord bot designed "
                    "to give you and your servers great functionality and stable performance.",
                    colour=Colour.BLUE,
                )
                .add_field(
                    "Guilds",
                    value=f"{len(guilds)} with {members_count} members",
                    inline=True,
                )
                .add_field(
                    name="Created",
                    value=format_datetime(context.bot.get_me().created_at, "R"),
                    inline=True,
                )
                .add_field(
                    name="Version",
                    value=(
                        f"{__version__!s} "
                        f"([`{__version__.hash}`](https://github.com/ShinshiDevs/Shinshi/commit/{__version__.hash}))"
                    ),
                    inline=True,
                )
                .set_thumbnail(context.bot.get_me().avatar_url)
                .set_footer(
                    f"You're located on #{context.guild.shard_id} shard ・ © 2024 Shinshi Developers Team"
                )
            )
        )
