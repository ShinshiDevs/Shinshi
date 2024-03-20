from typing import Tuple, Dict, Any

from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.workflows.constants import WORKFLOW_INTERACTABLES


class WorkflowMeta(type):
    def __new__(
        mcs, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]
    ):
        new_cls = super().__new__(mcs, name, bases, namespace)
        setattr(
            new_cls,
            WORKFLOW_INTERACTABLES,
            list(attr_value for _, attr_value in namespace.items()
                 if isinstance(attr_value, Interactable))
        )
        return new_cls
