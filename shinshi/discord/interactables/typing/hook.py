from typing import TYPE_CHECKING, TypeVar, Callable, Awaitable

if TYPE_CHECKING:
    from shinshi.discord.interactables.models.hook_result import HookResult
    from shinshi.discord.models.interaction_context import InteractionContext

HookT: TypeVar = TypeVar(
    "HookT", bound=Callable[["InteractionContext"], Awaitable["HookResult"]]
)
