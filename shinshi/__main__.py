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
import warnings

import orjson
from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent
from hikari.impl import CacheComponents, CacheSettings, HTTPSettings

from shinshi import RESOURCES_DIR
from shinshi.discord.bot import Bot
from shinshi.discord.interaction.interaction_processor import InteractionProcessor
from shinshi.discord.workflows import WorkflowManager
from shinshi.i18n import I18nProvider
from shinshi.workflows import general

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    warnings.warn(
        "Are you on Windows? Bruh. Uvloop has left the chat.."
        "If not, install uvloop by `poetry install --group unix`"
    )
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


i18n_provider = I18nProvider(RESOURCES_DIR / "i18n")
bot = Bot(
    token=os.environ.get("SHINSHI_DISCORD_TOKEN"),
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
workflow_manager = WorkflowManager(
    bot,
    i18n_provider,
    (
        general.InfoWorkflow,
        general.InviteWorkflow,
        general.SupportWorkflow,
        general.UserWorkflow,
    ),
)
interaction_processor = InteractionProcessor(bot, i18n_provider, workflow_manager)


@bot.listen(StartingEvent)
async def on_starting(_: StartingEvent) -> None:
    await i18n_provider.start()
    await workflow_manager.build_workflows()


@bot.listen(StartedEvent)
async def on_started(_: StartedEvent) -> None:
    await workflow_manager.sync_slash_commands()
    bot.event_manager.subscribe(
        InteractionCreateEvent, interaction_processor.proceed_interaction
    )


if __name__ == "__main__":
    bot.run()
