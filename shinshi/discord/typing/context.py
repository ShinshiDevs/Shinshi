from typing import TypeVar

from shinshi.discord.models.interaction_context import InteractionContext

ContextT = TypeVar("ContextT", bound=InteractionContext)
