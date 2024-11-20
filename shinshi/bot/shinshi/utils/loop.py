import os
import warnings
import asyncio

try:
    import uvloop
except ImportError:
    uvloop = None
    if os.name != "nt":
        warnings.warn("uvloop can't be used, because it's not installed")


def get_event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    if uvloop is not None:
        return uvloop.EventLoopPolicy()
    return asyncio.DefaultEventLoopPolicy()
