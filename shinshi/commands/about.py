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
from collections.abc import ValuesView
from typing import Any

from aurum.commands import SlashCommand
from aurum.commands.decorators import sub_command
from aurum.interactions import InteractionContext
from aurum.l10n import Localized
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild
from psutil import Process

from shinshi import __version__
from shinshi.utils.size import convert_size


class AboutCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("about", description=Localized("commands.about.description"))
        self.process: Process = Process()

    async def callback(self, context: InteractionContext) -> None:
        embed: Embed = Embed().set_thumbnail(context.bot.get_me().avatar_url)
        guilds: ValuesView[GatewayGuild] = context.bot.cache.get_guilds_view().values()
        ram_usage: tuple[int, str] = convert_size(self.process.memory_info().rss)
        formatting: dict[str, Any] = dict(
            version=str(__version__),
            hash=__version__.hash,
            hash_commit_url=f"https://github.com/ShinshiDevs/Shinshi/commit/{__version__.hash}",
            latency=f"{context.bot.heartbeat_latency * 1_000:.0f}",
            ram_usage=f"{ram_usage[0]} {ram_usage[1]}",
            guild_count=len(guilds),
            member_count=sum(guild.member_count for guild in guilds),
            shard_id=context.guild.shard_id,
        )
        for field in context.locale.get_seq("commands.about.embed.fields"):
            field["value"] = field["value"].format(**formatting)
            embed.add_field(**field)
        return await context.create_response(embed=embed)
