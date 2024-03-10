from dataclasses import dataclass
from typing import List

from shinshi.discord.workflows.workflow import Workflow


@dataclass
class WorkflowRepository:
    workflows: List[Workflow]
