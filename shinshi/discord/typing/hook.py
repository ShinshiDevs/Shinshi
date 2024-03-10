from typing import TypeVar, Callable

from shinshi.discord.data.hook_result import HookResult

HookT: TypeVar = TypeVar("HookT", bound=Callable[..., HookResult | None])  # TODO: Context?
