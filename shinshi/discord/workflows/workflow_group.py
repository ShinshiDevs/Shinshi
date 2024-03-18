from dataclasses import field, dataclass
from typing import Tuple

from shinshi.discord.workflows.workflow_base import WorkflowBase


@dataclass
class WorkflowGroup:
    workflows: Tuple[WorkflowBase, ...] = field(default_factory=list)
