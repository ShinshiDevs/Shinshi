from dataclasses import dataclass
from typing import Callable, Awaitable, Any

from shinshi.discord.context.typing import ContextT


@dataclass(kw_only=True)
class Interactable:
    callback: Callable[[ContextT, ...], Awaitable[Any]]

    defer: bool = False
    bound: bool = False

    is_ephemeral: bool = False
