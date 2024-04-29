from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

_LOGGER: Logger = logging.getLogger("shinshi.aio")


def set_event_policy() -> None:
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        _LOGGER.debug("event policy: uvloop")
    except ImportError:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
        _LOGGER.debug("event policy: default (asyncio)")
        _LOGGER.warning("please install uvloop if you are using a unix-type system.")
