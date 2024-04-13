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
from shinshi.discord.exceptions import InteractionException


class NoGuildIconException(InteractionException):
    async def callback(self) -> None:
        return await self.context.send_warning(
            self.context.i18n.get(
                "commands.guild.icon.exceptions.no_icon_exception",
            )
        )


class NoGuildSplashException(InteractionException):
    async def callback(self) -> None:
        return await self.context.send_warning(
            self.context.i18n.get(
                "commands.guild.splash.exceptions.no_splash_exception",
            )
        )


class NoGuildBannerException(InteractionException):
    async def callback(self) -> None:
        return await self.context.send_warning(
            self.context.i18n.get(
                "commands.guild.splash.exceptions.no_splash_exception",
            )
        )
