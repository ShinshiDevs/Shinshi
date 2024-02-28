import asyncio
import sys

import uvloop


def setup_event_policy() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        uvloop.install()
