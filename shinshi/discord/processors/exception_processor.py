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
from sentry_sdk import capture_exception, push_scope

from shinshi.discord.exceptions.interaction_exception import InteractionException
from shinshi.discord.interactables.command import Command
from shinshi.discord.interaction.interaction_context import InteractionContext


class ExceptionProcessor:
    async def proceed_exception(
        self, context: InteractionContext, exception: Exception
    ) -> None:
        if isinstance(exception, InteractionException):
            return await exception.callback()
        with push_scope() as scope:
            if isinstance(context.interactable, Command):
                scope.set_tag("command", context.interactable.qualname)
            if guild := context.interaction.get_guild():
                scope.set_tag("shard ID", guild.shard_id)
            scope.set_tag("user ID", context.interaction.user.id)
            scope.level = "warning"
            capture_exception(exception)
        return await context.send_error(
            context.i18n.get("exceptions.unknown_exception")
        )
