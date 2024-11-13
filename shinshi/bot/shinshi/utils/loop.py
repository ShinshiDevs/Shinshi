import os
import warnings
from asyncio import AbstractEventLoopPolicy, DefaultEventLoopPolicy

try:
    import uvloop
except ImportError:
    uvloop = None
    if os.name != "nt":
        warnings.warn("uvloop can't be used, because it's not installed")


def get_event_loop_policy() -> AbstractEventLoopPolicy:
    if uvloop is not None:
        return uvloop.EventLoopPolicy()
    return DefaultEventLoopPolicy()
