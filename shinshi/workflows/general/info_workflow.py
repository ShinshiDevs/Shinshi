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
from hikari.impl import (
    LinkButtonBuilder,
    MessageActionRowBuilder,
)

from shinshi import (
    ICONS_DIR,
    __copyright__,
    __github_url__,
    __license__,
    __support_url__,
)
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.utils.string import get_separated_number


class InfoWorkflow(Workflow):
    @command(description=Translatable("commands.info.description"), is_dm_enabled=True)
    async def info(self, context: InteractionContext) -> None:
        embed = (
            Embed(
                title=context.bot.me.username,
                url="https://github.com/ShinshiDevs",
                description=context.i18n.get(
                    "commands.info.embed.description",
                    {"shard": context.interaction.get_guild().shard_id + 1},
                ),
            )
            .set_thumbnail(context.bot.me.avatar_url)
            .set_author(
                name=context.i18n.get("commands.info.embed.author.name"),
                icon=ICONS_DIR / "information.webp",
            )
            .set_footer(text=f"{__copyright__} ({__license__})")
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.information.name"),
                value="\n".join(
                    context.i18n.get_list(
                        "commands.info.embed.fields.information.value",
                        {
                            "guilds": get_separated_number(
                                len(context.bot.cache.get_guilds_view())
                            ),
                            "latency": f"{round(context.bot.heartbeat_latency * 1000, 1)}ms",
                        },
                    )
                ),
            )
        )
        return await context.create_response(
            embed=embed,
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(label="Github", url=__github_url__),
                    LinkButtonBuilder(label="Support", url=__support_url__),
                ]
            ),
        )
