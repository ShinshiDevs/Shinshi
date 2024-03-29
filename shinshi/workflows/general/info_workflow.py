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

from shinshi import __copyright__, __license__
from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.decorators.slash_command import slash_command
from shinshi.discord.workflows.workflow_base import WorkflowBase
from shinshi.utils.icons import get_icon
from shinshi.utils.number import get_separated_number


class InfoWorkflow(WorkflowBase):
    @slash_command(
        description=Translatable("commands.info.description"), dm_enabled=True
    )
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
            .set_thumbnail(context.bot.me.make_avatar_url(size=512))
            .set_author(
                name=context.i18n.get("commands.info.embed.author.name"),
                icon=get_icon("information"),
            )
            .set_footer(text=f"{__copyright__} ({__license__})")
            .add_field(
                name=context.i18n.get("commands.info.embed.fields.information.name"),
                value="\n".join(
                    context.i18n.get_list(
                        "commands.info.embed.fields.information.value",
                        {
                            "guilds": get_separated_number(
                                context.bot.get_guild_count()
                            ),
                            "users": get_separated_number(
                                context.bot.get_member_count()
                            ),
                            "latency": f"{round(context.bot.heartbeat_latency * 1000, 1)}ms",
                        },
                    )
                ),
            )
        )
        return await context.create_response(embed=embed)
