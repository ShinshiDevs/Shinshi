from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

from hikari.intents import Intents
from hikari.internal import aio

from shinshi.discord.bot import Bot
from shinshi.ext.aio import set_event_policy
from shinshi.ext.dotenv import load_dotenv
from shinshi.ext.logging import configure_logging
from shinshi.i18n import I18nProvider

if TYPE_CHECKING:
    from logging import Logger

set_event_policy()
load_dotenv()
configure_logging(Path.cwd() / "config" / "logging.json")

logger: Logger = logging.getLogger("shinshi")
i18n: I18nProvider = I18nProvider(Path.cwd() / "resources" / "i18n")
bot: Bot = Bot(
    token=os.getenv("SHINSHI_DISCORD_TOKEN"), banner=None, intents=Intents.GUILDS
)

if __name__ == "__main__":
    logger.info("starting...")

    loop: asyncio.AbstractEventLoop = aio.get_or_make_loop()
    bot_task: asyncio.Task | None = None

    try:
        loop.run_until_complete(i18n.start())
        bot_task = loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("stopping...")
        loop.run_until_complete(bot.close())
        loop.run_until_complete(bot_task)
        bot_task = None
    except Exception as exception:
        logger.exception(
            "some exception occurred while working and it wasn't catched or while starting",
            exc_info=exception,
        )
    finally:
        logger.info("bye-bye, world, see you next session")
        loop.stop()
        loop.close()
        asyncio.set_event_loop(None)
