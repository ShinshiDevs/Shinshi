from dataclasses import field, dataclass
from typing import Tuple, Type

from shinshi.discord.workflows.workflow_base import WorkflowBase


@dataclass
class WorkflowGroup:
    workflows: Tuple[Type[WorkflowBase], ...] = field(default_factory=tuple)
