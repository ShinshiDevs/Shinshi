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
from hikari.impl import LinkButtonBuilder, MessageActionRowBuilder

from shinshi import __support_url__
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command


class SupportWorkflow(Workflow):
    @command(
        description=Translatable("commands.support.description"), is_dm_enabled=True
    )
    async def support(self, context: InteractionContext) -> None:
        return await context.create_response(
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=context.i18n.get("buttons.support.label"),
                        url=__support_url__,
                    )
                ]
            )
        )
