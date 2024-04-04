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

from shinshi.discord.exceptions import InteractionException


class WebhookCreationException(InteractionException):
    async def callback(self) -> None:
        return await self.context.create_response(
            content=self.context.i18n.get(
                "commands.say.exceptions.webhook_creation_exception"
            ),
            flags=MessageFlag.EPHEMERAL,
        )


class WebhookExecutionException(InteractionException):
    async def callback(self) -> None:
        return await self.context.create_response(
            content=self.context.i18n.get(
                "commands.say.exceptions.webhook_execution_exception"
            ),
            flags=MessageFlag.EPHEMERAL,
        )
