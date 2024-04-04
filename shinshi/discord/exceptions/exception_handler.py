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
from logging import getLogger

from shinshi.discord.bot.base_bot import BaseBot
from shinshi.discord.exceptions import InteractionException
from shinshi.discord.exceptions.unknown_exception import UnknownException
from shinshi.discord.models.interaction_context import InteractionContext


class ExceptionHandler:
    def __init__(self, bot: BaseBot) -> None:
        self.__logger = getLogger("shinshi.exceptions")
        self.bot = bot

    async def send_to_developers(self) -> None:
        ...

    async def proceed(self, exception: Exception, context: InteractionContext) -> None:
        if isinstance(exception, InteractionException):
            try:
                return await exception.callback()
            except Exception as exception:
                self.__logger.error(
                    "Cannot handle exception, because of another exception",
                    exc_info=exception,
                )
        else:
            await self.send_to_developers()
            return await UnknownException(context).callback()
