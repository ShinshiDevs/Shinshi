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
from hikari.commands import CommandOption, OptionType
from hikari.guilds import Role
from hikari.interactions import (
    CommandInteraction,
    InteractionChannel,
    InteractionMember,
)
from hikari.users import User


class CommandProcessor:
    def convert_command_option_value(
        self, interaction: CommandInteraction, option: CommandOption
    ) -> (
        User | InteractionMember | InteractionChannel | Role | str | int | float | None
    ):
        match option.type:
            case OptionType.STRING:
                return str(option.value)
            case OptionType.INTEGER:
                return int(option.value)
            case OptionType.BOOLEAN:
                return bool(option.value)
            case OptionType.USER:
                return interaction.resolved.members.get(
                    option.value, interaction.resolved.users.get(option.value)
                )
            case OptionType.CHANNEL:
                return interaction.resolved.channels.get(option.value)
            case OptionType.ROLE:
                return interaction.resolved.roles.get(option.value)
            case OptionType.MENTIONABLE:
                return (
                    interaction.resolved.members.get(option.value)
                    or interaction.resolved.users.get(option.value)
                    or interaction.resolved.channels.get(option.value)
                    or interaction.resolved.roles.get(option.value)
                )
            case OptionType.FLOAT:
                return float(option.value)
            case OptionType.ATTACHMENT:
                return interaction.resolved.attachments.get(option.value)
            case _:
                return
