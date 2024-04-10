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
from pathlib import Path
from typing import Any

from hikari.applications import Application
from hikari.impl import CacheSettings, GatewayBot
from hikari.users import OwnUser

from shinshi import __banner_extras__
from shinshi.discord.bot.cache import Cache
from shinshi.discord.bot.ux import print_banner


class Bot(GatewayBot):
    def __init__(self, token: str, cache_settings: CacheSettings, **kwargs):
        self.__application: Application | None = None
        self.__cache = Cache(self, cache_settings)
        super().__init__(
            token=token,
            banner=None,
            cache_settings=cache_settings,
            **kwargs,
        )
        print_banner(Path("resources", "banner.txt"), extra_args=__banner_extras__)

    async def get_application(self) -> Application:
        if self.__application is not None:
            return self.__application
        self.__application = await self.rest.fetch_application()
        return self.__application

    @property
    def application(self) -> Application:
        return self.__application

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user

    @property
    def cache(self) -> Cache:
        return self.__cache

    @property
    def _cache(self) -> Cache:
        return self.__cache

    @_cache.setter
    def _cache(self, ot: Any) -> None:  # type: ignore
        pass
