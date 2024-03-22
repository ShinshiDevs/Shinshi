from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from shinshi.discord.models.interaction_context import InteractionContext

ContextT = TypeVar("ContextT", bound="InteractionContext")
