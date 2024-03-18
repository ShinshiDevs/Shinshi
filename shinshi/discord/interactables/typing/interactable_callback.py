from typing import Callable, Awaitable, Any

from shinshi.discord.typing.context import ContextT

InteractableCallbackT = Callable[[ContextT, ...], Awaitable[Any]]
