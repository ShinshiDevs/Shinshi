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
import asyncio
import concurrent.futures
import os
import platform
import sys
from pathlib import Path

import orjson
import uvloop
from aiohttp import ClientTimeout, TCPConnector
from aiohttp.client import ClientSession
from hikari import events
from hikari.impl import CacheComponents, CacheSettings, HTTPSettings

from shinshi import __copyright__, __github_url__, __license__, __support_url__
from shinshi.discord.bot import BaseBot
from shinshi.i18n import I18nProvider

asyncio.set_event_loop_policy(
    uvloop.EventLoopPolicy()
    if sys.platform != "win32"
    else asyncio.DefaultEventLoopPolicy()
)


class Bot(BaseBot):
    def __init__(self) -> None:
        self.http_session: ClientSession | None = None
        self.i18n = I18nProvider()
        super().__init__(
            token=os.environ.get("SHINSHI_DISCORD_TOKEN"),
            banner=Path(os.getcwd(), "resources", "banner.txt"),
            banner_extras={
                "shinshi_license": __license__,
                "shinshi_copyright": __copyright__,
                "shinshi_github_url": __github_url__,
                "shinshi_support_url": __support_url__,
                "python_implementation": platform.python_implementation(),
                "python_version": platform.python_version(),
            },
            executor=concurrent.futures.ThreadPoolExecutor(),
            cache_settings=CacheSettings(
                components=CacheComponents.GUILDS,
                max_messages=100,
                max_dm_channel_ids=0,
            ),
            http_settings=HTTPSettings(enable_cleanup_closed=True),
            dumps=orjson.dumps,
            loads=orjson.loads,
        )

    @staticmethod
    def orjson_serialize(data: bytes) -> str:
        return orjson.dumps(data).decode("UTF-8")

    async def on_starting(self, _) -> None:
        self.http_session = ClientSession(
            connector=TCPConnector(),
            json_serialize=self.orjson_serialize,
            timeout=ClientTimeout(3),
        )
        await self.i18n.start()

    async def on_stopping(self, _) -> None:
        await self.http_session.close()


if __name__ == "__main__":
    bot = Bot()
    bot.event_manager.subscribe(events.StartingEvent, bot.on_starting)
    bot.event_manager.subscribe(events.StoppingEvent, bot.on_stopping)
    bot.run()
