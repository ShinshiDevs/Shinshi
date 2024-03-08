import asyncio


def create_loop() -> asyncio.AbstractEventLoop:
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop
