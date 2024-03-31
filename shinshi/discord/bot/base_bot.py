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
import concurrent.futures
import pathlib
import string
import sys
from typing import Any, Dict

import colorlog
from hikari.impl import GatewayBot, config
from hikari.intents import Intents
from hikari.internal import data_binding
from hikari.internal.ux import supports_color
from hikari.users import OwnUser

from shinshi.discord.bot.cache import Cache


class BaseBot(GatewayBot):
    def __init__(
        self,
        token: str,
        *,
        allow_color: bool = True,
        banner: pathlib.Path | None = None,
        banner_extras: Dict[str, Any] | None = None,
        suppress_optimization_warning: bool = False,
        executor: concurrent.futures.Executor | None = None,
        force_color: bool = False,
        cache_settings: config.CacheSettings | None = None,
        http_settings: config.HTTPSettings | None = None,
        dumps: data_binding.JSONEncoder = data_binding.default_json_dumps,
        loads: data_binding.JSONDecoder = data_binding.default_json_loads,
        intents: Intents = Intents.ALL_UNPRIVILEGED,
        auto_chunk_members: bool = True,
        logs: int | str = "INFO",
        max_rate_limit: float = 300.0,
        max_retries: int = 3,
        proxy_settings: config.ProxySettings | None = None,
        rest_url: str | None = None,
    ) -> None:
        if banner:
            self.__print_banner(
                banner, allow_color, force_color, extra_args=banner_extras
            )
        self.__cache = Cache(self, cache_settings)
        super().__init__(
            token=token,
            allow_color=allow_color,
            banner=None,
            suppress_optimization_warning=suppress_optimization_warning,
            executor=executor,
            force_color=force_color,
            cache_settings=cache_settings,
            http_settings=http_settings,
            dumps=dumps,
            loads=loads,
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            logs=logs,
            max_rate_limit=max_rate_limit,
            max_retries=max_retries,
            proxy_settings=proxy_settings,
            rest_url=rest_url,
        )

    @staticmethod
    def __print_banner(
        banner_file: pathlib.Path,
        allow_color: bool,
        force_color: bool,
        extra_args: Dict[str, Any],
    ) -> None:
        args: Dict[str, Any] = extra_args.copy()
        if supports_color(allow_color, force_color):
            args.update(colorlog.escape_codes.escape_codes)
        else:
            for code in colorlog.escape_codes.escape_codes:
                args[code] = ""

        with open(banner_file, "r", encoding="UTF-8") as stream:
            banner: str = string.Template(stream.read()).safe_substitute(args)
            sys.stdout.buffer.write(banner.encode("utf-8"))
            sys.stdout.flush()

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
    def _cache(self, ot: Any) -> None:
        pass

    def get_guild_count(self) -> int:
        return len(self.cache.get_guilds_view())

    def get_member_count(self) -> int:
        return sum(
            self.cache.get_guild(guild).member_count
            for guild in self.cache.get_guilds_view()
        )
