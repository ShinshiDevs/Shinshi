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
from hikari.impl import GatewayBot
from hikari.users import OwnUser

from shinshi.discord.bot.cache import Cache


class Bot(GatewayBot):
    def __init__(self, token: str | None, **kwargs) -> None:
        if not token:
            raise ValueError("Bot cannot be started without token")
        self.__cache = Cache(self)
        super().__init__(
            token=token,
            banner=None,
            cache_settings=self.__cache.settings,
            **kwargs,
        )

    @property
    def me(self) -> OwnUser:
        if user := self.get_me():
            return user
        raise RuntimeError("Cannot access own user")

    @property
    def cache(self) -> Cache:
        return self.__cache

    @property
    def _cache(self) -> Cache:
        return self.__cache

    @_cache.setter
    def _cache(self, ot: Cache) -> None:
        return
