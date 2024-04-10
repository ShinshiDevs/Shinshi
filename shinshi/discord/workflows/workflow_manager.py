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
from typing import Dict, List, Sequence

from hikari.commands import CommandChoice, CommandOption, OptionType
from hikari.impl import SlashCommandBuilder

from shinshi.discord.bot import Bot
from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.group import Group, SubGroup
from shinshi.discord.interactables.options import Option
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.i18n import I18nProvider


class WorkflowManager:
    def __init__(
        self,
        bot: Bot,
        i18n_provider: I18nProvider,
        workflows: Sequence[Workflow],
    ) -> None:
        self.bot = bot
        self.i18n_provider = i18n_provider
        self.workflows = workflows

        self.commands: Dict[str, Command | Group] = {}
        self.slash_command_builders: List[SlashCommandBuilder] = []

    async def build_workflows(self) -> None:
        for workflow_cls in self.workflows:
            workflow: Workflow = workflow_cls()
            await workflow.start()

            for command in workflow.get_commands():
                if command.group:
                    self.commands[command.group.name] = command.group
                else:
                    self.commands[command.name] = command
                    self.slash_command_builders.append(
                        self.get_command_builder(command)
                    )

        for group in [
            group for group in self.commands.values() if isinstance(group, Group)
        ]:
            self.slash_command_builders.append(self.get_group_builder(group))

    async def sync_slash_commands(self) -> None:
        await self.bot.rest.set_application_commands(
            await self.bot.get_application(),
            self.slash_command_builders,
        )

    def get_group_builder(self, group: Group) -> SlashCommandBuilder:
        builder: SlashCommandBuilder = self.get_command_builder_base(group)
        for command in group.commands.values():
            builder.add_option(self.build_sub_command(command))
        for sub_group in group.sub_groups.values():
            builder.add_option(self.build_sub_group(sub_group))
        return builder

    def get_command_builder(self, command: Command) -> SlashCommandBuilder:
        builder: SlashCommandBuilder = self.get_command_builder_base(command)
        for option in command.options:
            builder.add_option(self.build_option(option))
        return builder

    def get_command_builder_base(self, command: Command | Group) -> SlashCommandBuilder:
        builder: SlashCommandBuilder = (
            self.bot.rest.slash_command_builder(
                name=command.name,
                description="-",
            )
            .set_default_member_permissions(command.default_member_permissions)
            .set_is_dm_enabled(command.is_dm_enabled)
            .set_is_nsfw(command.is_nsfw)
        )
        if isinstance(command, Command):
            description: Translatable = self.get_translatable_description(
                command.description
            )
            builder.set_description(description.fallback)
            builder.set_description_localizations(description.translates)
        return builder

    def get_translatable_description(
        self, description: Translatable | str | None
    ) -> Translatable:
        description: Translatable = (
            Translatable(fallback=description or "No description")
            if not isinstance(description, Translatable)
            else description
        )
        description.build(self.i18n_provider)
        return description

    def build_option(self, option: Option) -> CommandOption:
        description: Translatable = self.get_translatable_description(
            option.description
        )
        choices: List[CommandChoice] = [
            CommandChoice(name=choice.name, value=choice.value)
            for choice in option.choices
        ]
        return CommandOption(
            type=option.type,
            name=option.name,
            description=description.fallback,
            is_required=option.is_required,
            choices=choices,
            channel_types=getattr(option, "channel_types", None),
            autocomplete=option.is_autocomplete,
            min_value=getattr(option, "min_value", None),
            max_value=getattr(option, "max_value", None),
            description_localizations=description.translates,
            min_length=getattr(option, "min_length", None),
            max_length=getattr(option, "max_length", None),
        )

    def build_sub_command(self, command: Command) -> CommandOption:
        description: Translatable = self.get_translatable_description(
            command.description
        )
        return CommandOption(
            type=OptionType.SUB_COMMAND,
            name=command.name,
            description=description.fallback,
            options=[self.build_option(option) for option in command.options],
            description_localizations=description.translates,
        )

    def build_sub_group(self, sub_group: SubGroup) -> CommandOption:
        return CommandOption(
            type=OptionType.SUB_COMMAND_GROUP,
            name=sub_group.name,
            description="-",
            options=[self.build_sub_command(command) for command in sub_group.commands],
        )

    def get_command(
        self,
        group_name: str | None,
        subgroup_name: str | None,
        command_name: str | None,
    ) -> Command | None:
        group = self.commands.get(group_name) if group_name else None
        if group and isinstance(group, Group):
            subgroup = group.sub_groups.get(subgroup_name) if subgroup_name else None
            if subgroup and isinstance(subgroup, SubGroup):
                return subgroup.commands.get(command_name)
            return group.commands.get(command_name)
        return self.commands.get(command_name)
