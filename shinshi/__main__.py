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
from logging.config import dictConfig
from os import getenv

import orjson
import sentry_sdk
from hikari.events import (
    InteractionCreateEvent,
    ShardReadyEvent,
    StartedEvent,
    StartingEvent,
)
from hikari.impl import HTTPSettings
from hikari.presences import Activity, ActivityType

from shinshi import CONFIG_DIR, RESOURCES_DIR, __banner_extras__
from shinshi.discord.bot import Bot
from shinshi.discord.interaction import InteractionProcessor
from shinshi.discord.workflows import WorkflowManager
from shinshi.dotenv.load import load_dotenv
from shinshi.i18n import I18nProvider
from shinshi.workflows import workflows

load_dotenv(".env")

with open(CONFIG_DIR / "logging.json", encoding="UTF-8") as stream:
    dictConfig(orjson.loads(stream.read()))

try:
    asyncio.set_event_loop_policy(__import__("uvloop").EventLoopPolicy())
except ImportError:
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

bot = Bot(
    token=getenv("SHINSHI_DISCORD_TOKEN"),
    http_settings=HTTPSettings(enable_cleanup_closed=True),
)
i18n_provider = I18nProvider(RESOURCES_DIR / "i18n")
workflow_manager = bot.workflow_manager = WorkflowManager(
    bot,
    i18n_provider,
    workflows,
)
bot.event_manager.subscribe(
    InteractionCreateEvent,
    InteractionProcessor(bot, i18n_provider, workflow_manager).proceed_interaction,
)


@bot.listen()
async def on_starting(_: StartingEvent) -> None:
    await i18n_provider.start()
    await workflow_manager.build_workflows()


@bot.listen()
async def on_shard_start(event: ShardReadyEvent):
    await event.shard.update_presence(
        activity=Activity(
            type=ActivityType.CUSTOM,
            state=f"Shard #{event.shard.id} with {len(event.unavailable_guilds)} guilds",
            name="-",
        )
    )


@bot.listen()
async def on_started(_: StartedEvent) -> None:
    await bot.fetch_application()
    await workflow_manager.sync_slash_commands()


def main() -> None:
    bot.print_banner("shinshi", True, False, __banner_extras__)
    sentry_sdk.init(
        dsn=getenv("SHINSHI_SENTRY_DSN"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        keep_alive=True,
    )
    bot.run(
        check_for_updates=False,
        coroutine_tracking_depth=5,
    )


if __name__ == "__main__":
    main()
