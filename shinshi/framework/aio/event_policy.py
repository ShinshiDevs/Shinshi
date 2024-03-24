import asyncio
import sys

import uvloop


def setup_event_policy() -> None:
    asyncio.set_event_loop_policy(
        uvloop.EventLoopPolicy() if sys.platform == "win32"
        else asyncio.DefaultEventLoopPolicy()
    )
