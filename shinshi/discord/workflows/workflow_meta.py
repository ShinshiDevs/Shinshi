from typing import Tuple, Dict, Any

from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.workflows.constants import WORKFLOW_INTERACTABLES


class WorkflowMeta:
    def __new__(cls, name: str, bases: Tuple[type], attrs: Dict[str, Any], *args, **kwargs):
        setattr(
            cls,
            WORKFLOW_INTERACTABLES,
            list(base for base in bases if isinstance(base, Interactable))
        )
        return super().__new__(cls, name, bases, attrs, *args, **kwargs)
