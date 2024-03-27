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
from hikari.commands import OptionType
from hikari.users import User

from shinshi.discord.models.interaction_context import InteractionContext
from shinshi.discord.workflows.decorators.slash_command import slash_command
from shinshi.discord.workflows.interactables.options.option import Option
from shinshi.discord.workflows.workflow_base import WorkflowBase


class TestWorkflow(WorkflowBase):
    @slash_command(
        dm_enabled=True,
        options=(Option(type=OptionType.USER, name="something"),),
    )
    async def test(self, context: InteractionContext, something: User) -> None:
        print(type(something))
        return await context.create_response(content=something)
