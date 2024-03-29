# Copyright (C) 2024 Shinshi Developers Team
#
# This file is part of Shinshi.
#
# Shinshi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinshi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Shinshi.  If not, see <https://www.gnu.org/licenses/>.
from abc import abstractmethod
from typing import Sequence, Tuple

from shinshi.discord.workflows.constants import _WORKFLOW_PREDEFINED_INTERACTABLES
from shinshi.discord.workflows.interactables.commands.command import Command
from shinshi.discord.workflows.interactables.interactable import Interactable
from shinshi.discord.workflows.workflow_meta import WorkflowMeta


class WorkflowBase(metaclass=WorkflowMeta):
    def __init__(
        self,
        *,
        name: str | None = None,
    ) -> None:
        self.name: str = name or type(self).__name__
        self.interactables: Tuple[Interactable, ...] = getattr(
            self, _WORKFLOW_PREDEFINED_INTERACTABLES, ()
        )

    @abstractmethod
    async def start(self) -> None:
        ...

    def get_commands(self) -> Sequence[Command]:
        return tuple(
            interactable
            for interactable in self.interactables
            if isinstance(interactable, Command)
        )
