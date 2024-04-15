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
from hikari.permissions import Permissions

from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.utils.oauth import oauth_url


class InviteWorkflow(Workflow):
    @command(
        description=Translatable("commands.invite.description"), is_dm_enabled=True
    )
    async def invite(self, context: InteractionContext) -> None:
        return await context.create_response(
            component=MessageActionRowBuilder(
                components=[
                    LinkButtonBuilder(
                        label=context.i18n.get(
                            "commands.invite.buttons.no_permissions.label"
                        ),
                        url=oauth_url(context.interaction.application_id),
                    ),
                    LinkButtonBuilder(
                        label=context.i18n.get(
                            "commands.invite.buttons.administrator.label"
                        ),
                        url=oauth_url(
                            context.interaction.application_id,
                            permissions=Permissions.ADMINISTRATOR,
                        ),
                    ),
                ]
            )
        )
