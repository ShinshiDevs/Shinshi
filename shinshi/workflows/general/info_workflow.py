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
import platform
from datetime import datetime

import psutil
from hikari._about import __version__
from hikari.embeds import Embed

from shinshi import (
    IMAGES_DIR,
    __author__,
    __github_url__,
    __license__,
)
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.ext.colour import Colour
from shinshi.utils.string import get_separated_number

components: tuple[tuple[str, str, str], ...] = (
    (
        platform.python_implementation(),
        platform.python_version(),
        "https://github.com/python/cpython",
    ),
    ("hikari", __version__, "https://github.com/hikari-py/hikari"),
)


class InfoWorkflow(Workflow):
    @command(
        description=Translatable("commands.info.description"),
        is_dm_enabled=True,
        is_defer=True,
    )
    async def info(self, context: InteractionContext) -> None:
        process = psutil.Process()
        embed = (
            Embed(
                title=context.bot.me.username,
                url=__github_url__,
                colour=Colour.DARK,
            )
            .set_author(
                name=context.i18n.get("commands.info.embed.author.name"),
                icon=IMAGES_DIR / "info.webp",
            )
            .set_footer(
                text=f"{__license__} {datetime.now().year} {__author__}",
                icon=IMAGES_DIR / "copyright.webp",
            )
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.libraries.name"),
                value="\n".join(
                    [
                        f"[{component} {version}]({url})"
                        for component, version, url in components
                    ]
                ),
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.guilds.name"),
                value=get_separated_number(len(context.bot.cache.get_guilds_view())),
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.members.name"),
                value=get_separated_number(
                    sum(
                        guild.member_count  # type: ignore  # fix soon, because sum need bool, not int
                        for guild in context.bot.cache.get_guilds_view().values()
                    )
                ),
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.latency.name"),
                value=f"{round(context.bot.heartbeat_latency * 1000, 2)}ms",
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.ram.name"),
                value=f"{round(process.memory_full_info().rss / (2 ** 20), 1)} MB "
                f"({round(process.memory_percent(), 2)}%)",
                inline=True,
            )
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.cpu.name"),
                value=f"{round(process.cpu_percent(interval=1), 2)}%",
                inline=True,
            )
        )
        return await context.create_response(embed=embed)
