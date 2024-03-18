from typing import TypeVar, Callable, Awaitable

from shinshi.discord.interactables.models.hook_result import HookResult

HookT: TypeVar = TypeVar("HookT", bound=Callable[[...], Awaitable[HookResult | None]])
