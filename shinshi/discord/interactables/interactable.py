from dataclasses import dataclass

from shinshi.discord.interactables.typing.interactable_callback import InteractableCallbackT


@dataclass(kw_only=True)
class Interactable:
    callback: InteractableCallbackT

    is_defer: bool = False
    is_bound: bool = False
    """Is this interaction is personal for one user and not hidden from other."""
    is_ephemeral: bool = False
