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
from typing import Any

from hikari.commands import OptionType
from hikari.files import Resourceish
from hikari.guilds import Role
from hikari.interactions import (
    CommandInteraction,
    CommandInteractionOption,
    InteractionChannel,
    InteractionMember,
)


def get_interaction_argument(
    interaction: CommandInteraction, option: CommandInteractionOption
) -> InteractionMember | InteractionChannel | Resourceish | Role | Any | None:
    if not interaction.resolved:
        raise ValueError("Interaction don't have resolved data")
    match option.type:
        case OptionType.USER:
            if interaction.resolved.members:
                return interaction.resolved.members.get(option.value)  # type: ignore
            if interaction.resolved.users:
                return interaction.resolved.users.get(option.value)  # type: ignore
            return None
        case OptionType.CHANNEL:
            return interaction.resolved.channels.get(option.value)  # type: ignore
        case OptionType.ROLE:
            return interaction.resolved.roles.get(option.value)  # type: ignore
        case OptionType.MENTIONABLE:
            if interaction.resolved.members:
                return interaction.resolved.members.get(option.value)  # type: ignore
            if interaction.resolved.roles:
                return interaction.resolved.roles.get(option.value)  # type: ignore
            return None
        case OptionType.ATTACHMENT:
            return interaction.resolved.attachments.get(option.value)  # type: ignore
        case _:
            return option.value


# there's many ignore, because mypy want me to override dict.get for this
# but, i don't want to do this, so ignore this's a best way, to continue do normal things
