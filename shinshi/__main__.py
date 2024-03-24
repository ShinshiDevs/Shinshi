import asyncio
import os
from typing import Any, Dict

import orjson
import yaml
from hikari.impl import config

from shinshi import __copyright__, __github__, __license__, __support__, logger
from shinshi.constants import RESOURCES_DIR, SECRETS_PATH
from shinshi.discord.bot import Bot
from shinshi.framework.aio.loop import create_loop
from shinshi.framework.di.injector import DI
from shinshi.framework.dotenv import load_dotenv
from shinshi.framework.events import event_manager
from shinshi.framework.events.lifetime_events import StartingEvent, StoppingEvent
from shinshi.framework.http import HttpPoolClient
from shinshi.framework.i18n import I18nProvider

load_dotenv(SECRETS_PATH / "app.env")

workflow_manager: None = None
interaction_processor: None = None
bot: Bot = Bot(
    token=os.environ.get("SHINSHI_DISCORD_TOKEN"),
    banner=None,
    loads=orjson.loads,
    dumps=orjson.dumps,
    http_settings=config.HTTPSettings(enable_cleanup_closed=True)
)

with open(RESOURCES_DIR / "emojis.yaml", "rb") as stream:
    emojis: Dict[str, Any] = yaml.load(stream, Loader=yaml.CLoader)
    DI.store(emojis, "emojis.yaml")
DI.store(I18nProvider(RESOURCES_DIR / "i18n"))
DI.store(HttpPoolClient())

bot.print_banner(
    __package__,
    True,
    False,
    {
        "shinshi_copyright": __copyright__,
        "shinshi_license": __license__,
        "shinshi_discord_invite": __support__,
        "shinshi_github_url": __github__,
    }
)

loop: asyncio.AbstractEventLoop = create_loop()
try:
    logger.info("Starting...")
    loop.run_until_complete(event_manager.emit(StartingEvent))
    loop.run_until_complete(bot.start())
    loop.run_forever()
except KeyboardInterrupt:
    logger.info("Stopping....")
    loop.run_until_complete(event_manager.emit(StoppingEvent))
    loop.run_until_complete(bot.close())
finally:
    loop.close()
