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
from enum import Enum

from hikari.snowflakes import Snowflake

from shinshi.discord.interaction.interaction_context import InteractionContext


class BucketType(Enum):
    NONE = 0
    USER = 1
    GUILD = 2
    MEMBER = 3

    def __call__(
        self, context: InteractionContext
    ) -> Snowflake | tuple[Snowflake, ...]:
        return {
            BucketType.NONE: (lambda _: None),
            BucketType.USER: (lambda _context: _context.interaction.guild_id),
            BucketType.GUILD: (lambda _context: _context.interaction.user.id),
            BucketType.MEMBER: lambda _context: (
                _context.interaction.guild_id,
                _context.interaction.member.id,
            ),
        }[self](context)
