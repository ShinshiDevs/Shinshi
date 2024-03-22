from typing import Tuple

from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.workflows.constants import WORKFLOW_INTERACTABLES
from shinshi.discord.workflows.workflow_meta import WorkflowMeta


class WorkflowBase(metaclass=WorkflowMeta):
    def __init__(
        self,
        *,
        name: str | None = None,
    ) -> None:
        self.name: str = name or type(self).__name__
        self.interactables: Tuple[Interactable, ...] = getattr(self, WORKFLOW_INTERACTABLES, [])
