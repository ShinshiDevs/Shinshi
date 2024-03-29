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
import os
import platform
from pathlib import Path

import orjson
import uvloop
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from hikari.applications import Application
from hikari.events.interaction_events import InteractionCreateEvent
from hikari.events.lifetime_events import StartedEvent, StartingEvent, StoppingEvent
from hikari.impl import CacheComponents, CacheSettings, HTTPSettings

from shinshi import __copyright__, __github_url__, __license__, __support_url__
from shinshi.discord.bot import BaseBot
from shinshi.discord.interaction_processor import InteractionProcessor
from shinshi.discord.workflows.workflow_manager import WorkflowManager
from shinshi.i18n import I18nProvider
from shinshi.workflows.general import InfoWorkflow, UserWorkflow
from shinshi.workflows.general.test_workflow import TestWorkflow

asyncio.set_event_loop_policy(
    uvloop.EventLoopPolicy()
    if platform.system() != "Windows"
    else asyncio.DefaultEventLoopPolicy()
)


class Bot(BaseBot):
    def __init__(self) -> None:
        self.http_session: ClientSession | None = None
        self.i18n = I18nProvider()
        self.workflow_manager = WorkflowManager(
            bot=self,
            i18n_provider=self.i18n,
            workflows=(InfoWorkflow, UserWorkflow, TestWorkflow),
        )
        self.interaction_processor = InteractionProcessor(
            bot=self, i18n_provider=self.i18n, workflow_manager=self.workflow_manager
        )
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
            cache_settings=CacheSettings(
                components=CacheComponents.ME
                | CacheComponents.GUILDS
                | CacheComponents.MEMBERS
                | CacheComponents.ROLES,
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

    async def on_starting(self, _: StartingEvent) -> None:
        self.http_session = ClientSession(
            connector=TCPConnector(),
            json_serialize=self.orjson_serialize,
            timeout=ClientTimeout(3),
        )
        await self.i18n.start()
        await self.workflow_manager.build_workflows()

    async def on_started(self, _: StartedEvent) -> None:
        application: Application = await self.rest.fetch_application()
        await self.workflow_manager.sync_slash_commands(application)
        self.event_manager.subscribe(InteractionCreateEvent, self.on_interaction)

    async def on_stopping(self, _: StoppingEvent) -> None:
        await self.http_session.close()

    async def on_interaction(self, event: InteractionCreateEvent) -> None:
        await self.interaction_processor.proceed(event.interaction)


if __name__ == "__main__":
    bot = Bot()
    bot.event_manager.subscribe(StartingEvent, bot.on_starting)
    bot.event_manager.subscribe(StartedEvent, bot.on_started)
    bot.event_manager.subscribe(StoppingEvent, bot.on_stopping)
    bot.run()
