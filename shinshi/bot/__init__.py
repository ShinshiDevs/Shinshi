from concurrent.futures import ThreadPoolExecutor
from os import environ

from hikari.impl import HTTPSettings

from shinshi import intents
from .structure import Bot, Cache

bot: Bot = Bot(
    token=environ.get("SHINSHI_DISCORD_TOKEN"),
    banner=None,
    executor=ThreadPoolExecutor(),
    intents=intents,
    cache_settings=Cache.settings,
    http_settings=HTTPSettings(
        enable_cleanup_closed=False
    ),
    logs={
        "loggers": {
            "hikari.gateway": {"level": "DEBUG"},
            "hikari.ratelimits": {"level": "TRACE_HIKARI"},
        },
    }
)
