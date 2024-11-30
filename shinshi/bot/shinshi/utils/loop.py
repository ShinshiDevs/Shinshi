import asyncio
import os
import warnings

try:
    import uvloop
except ImportError:
    uvloop = None
    if os.name != "nt":
        warnings.warn("uvloop can't be used, because it's not installed", stacklevel=0)


def get_event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    if uvloop is not None:
        return uvloop.EventLoopPolicy()
    return asyncio.DefaultEventLoopPolicy()
