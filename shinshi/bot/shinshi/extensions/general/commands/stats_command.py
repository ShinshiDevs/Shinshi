import platform
from typing import ValuesView

from aurum.commands import SlashCommand
from hikari.guilds import GatewayGuild
from hikari.embeds import Embed
from humanize import naturalsize
from psutil import Process

from shinshi import __version_info__
from shinshi.framework.context.context import Context
from shinshi.enums.colour import Colour
from shinshi.utils.icons import get_icon
from shinshi.utils.timestamp import format_timestamp
from shinshi.framework.i18n.localized import Localized


class StatsCommand(SlashCommand):
    def __init__(self) -> None:
        self.process: Process = Process()
        super().__init__(name="stats", description=Localized("commands.stats.description"), is_dm_enabled=True)

    async def callback(self, context: Context) -> None:
        guilds: ValuesView[GatewayGuild] = context.bot.cache.get_guilds_view().values()
        members_count: int = sum(guild.member_count or 0 for guild in guilds)
        embed: Embed = (
            Embed(colour=Colour.GREY)
            .set_author(name=context.locale.get("commands.stats.embed.title"), icon=get_icon("server.webp"))
            .add_field(
                name=context.locale.get("commands.stats.fields.version"),
                value=(
                    f"[{__version_info__.version}]"
                    f"(https://github.com/ShinshiDevs/Shinshi/releases/tag/{__version_info__.version}) "
                    f"([`{__version_info__.git_sha}`]"
                    f"(https://github.com/ShinshiDevs/Shinshi/commit/{__version_info__.git_sha}))"
                ),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.uptime"),
                value=format_timestamp(context.bot.uptime or 0, "R"),
                inline=True,
            )
            .add_field(name=context.locale.get("commands.stats.fields.system"), value=platform.system(), inline=True)
            .add_field(
                name=context.locale.get("commands.stats.fields.latency"),
                value=f"{context.bot.heartbeat_latency * 1_000:.1f}ms",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.cpu_usage"),
                value=f"{self.process.cpu_percent():.2f}%",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.stats.fields.memory_usage"),
                value=naturalsize(self.process.memory_info().rss),
                inline=True,
            )
            .add_field(name=context.locale.get("commands.stats.fields.guilds"), value=str(len(guilds)), inline=True)
            .add_field(name=context.locale.get("commands.stats.fields.members"), value=str(members_count), inline=True)
            .add_field(
                name=context.locale.get("commands.stats.fields.channels"),
                value=str(len(context.bot.cache.get_guild_channels_view())),
                inline=True,
            )
        )

        if context.guild is not None:
            embed.description = context.locale.get(
                "commands.stats.embed.description",
                {"shard_id": context.guild.shard_id or 0 + 1, "shard_count": context.bot.shard_count},
            )

        return await context.create_response(embed=embed)
