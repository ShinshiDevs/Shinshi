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
from hikari.messages import MessageFlag
from hikari.users import User

from shinshi.discord.exceptions import InteractionException
from shinshi.discord.models.interaction_context import InteractionContext


class UserAvatarAvailabilityException(InteractionException):
    def __init__(self, context: InteractionContext, user: User, *args) -> None:
        self.user = user
        super().__init__(context, *args)

    async def callback(self) -> None:
        return await self.context.create_response(
            content=self.context.i18n.get(
                "commands.user.avatar.exceptions.no_avatar_exception",
                {
                    "user": self.user.mention,
                },
            ),
            user_mentions=False,
            flags=MessageFlag.EPHEMERAL,
        )
