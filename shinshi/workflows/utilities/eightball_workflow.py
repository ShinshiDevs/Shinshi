#  Copyright (C) 2024 Shinshi Developers Team
#
#  This file is part of Shinshi.
#
#  Shinshi is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Shinshi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Shinshi.  If not, see <https://www.gnu.org/licenses/>.
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
import hashlib
from random import Random

from hikari.commands import OptionType

from shinshi.discord.interactables.options import StringOption
from shinshi.discord.interaction import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command


class EightBallWorkflow(Workflow):
    def get_seed(self, question: str) -> int:
        return int(hashlib.md5(question.encode("utf-8")).hexdigest(), 16)

    @command(
        name="8ball",
        description=Translatable("commands.8ball.description"),
        options=[
            StringOption(
                type=OptionType.STRING,
                name="question",
                description=Translatable(
                    "commands.8ball.arguments.question.description"
                ),
            )
        ],
    )
    async def eightball(self, context: InteractionContext, question: str) -> None:
        random = Random(self.get_seed(question))
        await context.create_response(
            random.choice(context.i18n.get_list("commands.8ball.answers"))
        )
