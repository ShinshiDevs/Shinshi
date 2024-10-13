import asyncio
import os
import warnings

if os.name == "nt":
    try:
        import winloop
    except ImportError:
        winloop = None
        warnings.warn("winloop can't be used, because it's not installed")

    def setup_event_loop_policy() -> None:
        if winloop:
            asyncio.set_event_loop_policy(winloop.WindowsProactorEventLoopPolicy())
        else:
            asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
else:
    try:
        import uvloop
    except ImportError:
        uvloop = None
        warnings.warn("uvloop can't be used, because it's not installed")

    def setup_event_loop_policy() -> None:
        if uvloop:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        else:
            asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
