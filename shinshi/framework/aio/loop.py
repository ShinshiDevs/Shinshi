import asyncio

from shinshi.framework.aio.event_policy import setup_event_policy


def create_loop() -> asyncio.AbstractEventLoop:
    setup_event_policy()
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop
