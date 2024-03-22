import asyncio
import os

import orjson
from hikari.impl import config

from shinshi.aio.loop import create_loop
from shinshi.constants import SECRETS_PATH
from shinshi.dotenv import load_dotenv

load_dotenv(SECRETS_PATH / "app.env")

if __name__ == '__main__':
    import shinshi
    from shinshi.discord.bot import Bot
    from shinshi.events import event_manager
    from shinshi.events.lifetime_events import StartingEvent, StoppingEvent

    workflow_manager: None = None
    interaction_processor: None = None
    bot: Bot = Bot(
        token=os.environ.get("SHINSHI_DISCORD_TOKEN"),
        banner=None,
        loads=orjson.loads,
        dumps=orjson.dumps,
        http_settings=config.HTTPSettings(enable_cleanup_closed=True)
    )

    bot.print_banner(
        shinshi.__name__,
        True,
        False,
        {
            "shinshi_copyright": shinshi.__copyright__,
            "shinshi_license": shinshi.__license__,
            "shinshi_discord_invite": shinshi.__support__,
            "shinshi_github_url": shinshi.__github__,
        }
    )

    loop: asyncio.AbstractEventLoop = create_loop()
    try:
        shinshi.logger.info("Starting...")
        loop.run_until_complete(event_manager.emit(StartingEvent))
        loop.run_until_complete(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        shinshi.logger.info("Stopping....")
        loop.run_until_complete(event_manager.emit(StoppingEvent))
        loop.run_until_complete(bot.close())
        loop.stop()
    finally:
        loop.close()
