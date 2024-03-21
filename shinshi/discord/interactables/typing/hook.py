from typing import TypeVar, Callable, Awaitable

HookT: TypeVar = TypeVar(
    "HookT", bound=Callable[["InteractionContext"], Awaitable["HookResult"]]
)
