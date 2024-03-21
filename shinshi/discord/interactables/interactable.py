from dataclasses import dataclass

from shinshi.discord.interactables.typing.interactable_callback import InteractableCallbackT


@dataclass(kw_only=True)
class Interactable:
    callback: InteractableCallbackT

    is_defer: bool = False
    is_bound: bool = False
    """Is interaction not hidden and only for one user."""
    is_ephemeral: bool = False
