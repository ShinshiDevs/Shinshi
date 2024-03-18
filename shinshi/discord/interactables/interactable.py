from dataclasses import dataclass

from shinshi.discord.interactables.typing.interactable_callback import InteractableCallbackT


@dataclass(kw_only=True)
class Interactable:
    callback: InteractableCallbackT

    defer: bool = False
    bound: bool = False

    is_ephemeral: bool = False
