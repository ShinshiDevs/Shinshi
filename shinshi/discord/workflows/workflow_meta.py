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
from typing import Self

from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.workflows.constants import (
    INTERACTABLE_WORKFLOW_INSTANCE,
    WORKFLOW_INTERACTABLES,
)


class WorkflowMeta(type):
    def __new__(mcs, name, bases, attrs) -> Self:
        cls = super().__new__(mcs, name, bases, attrs)
        setattr(cls, WORKFLOW_INTERACTABLES, [])
        for name, obj in attrs.items():
            if isinstance(obj, Interactable):
                setattr(obj, INTERACTABLE_WORKFLOW_INSTANCE, cls)
                getattr(cls, WORKFLOW_INTERACTABLES).append(obj)
        return cls
