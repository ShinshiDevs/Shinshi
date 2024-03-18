from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List

from shinshi.discord.interactables.interactable import Interactable


@dataclass
class Group:
    name: str
    children: List[Group | Interactable, ...] = field(default_factory=list)

    def child(self) -> Callable[[Interactable], None]:
        def decorator(interactable: Interactable) -> None:
            self.children.append(interactable)

        return decorator
