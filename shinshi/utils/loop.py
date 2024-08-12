import asyncio
import warnings

try:
    import uvloop
except ImportError:
    uvloop = None
    warnings.warn("Uvloop cant be used, because it's not installed")


def install_uvloop() -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
