from collections.abc import Callable
from os import environ


def getenv[T, DefaultT](key: str, *, default: DefaultT | None = None, return_type: Callable[..., T] = str) -> DefaultT | T:
    value: str | None = environ.get(key)
    if not value:
        if default:
            return default
        raise RuntimeError(f"Variable with name `{key}` is not defined in environment")
    return return_type(value)
