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
import logging
from typing import Type

from hikari.api import SlashCommandBuilder
from hikari.commands import CommandChoice, CommandOption, OptionType

from shinshi.discord.bot import Bot
from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.group import Group, SubGroup
from shinshi.discord.interactables.options import Option
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.i18n import I18nProvider


class WorkflowManager:
    __slots__: tuple[str, ...] = (
        "__logger",
        "bot",
        "i18n_provider",
        "workflows",
        "commands",
        "slash_command_builders",
    )

    def __init__(
        self,
        bot: Bot,
        i18n_provider: I18nProvider,
        workflows: tuple[Type[Workflow], ...],
    ) -> None:
        self.__logger = logging.getLogger("shinshi.workflows")

        self.bot = bot
        self.i18n_provider = i18n_provider
        self.workflows = workflows

        self.commands: dict[str, Command | Group] = {}
        self.slash_command_builders: list[SlashCommandBuilder] = []

    async def build_workflows(self) -> None:
        for workflow_cls in self.workflows:
            workflow = workflow_cls()
            await workflow.start()
            for command in workflow.get_commands():
                if command.group:
                    self.commands.update({command.group.name: command.group})
                    continue
                self.commands.update({command.name: command})
            self.__logger.debug("loaded %s", workflow_cls.__qualname__)
        self.__logger.info("loaded commands %s", ", ".join(self.commands.keys()))

    async def sync_slash_commands(self) -> None:
        for command in self.commands.values():
            self.slash_command_builders.append(
                (
                    self.get_group_builder(command)
                    if isinstance(command, Group)
                    else self.get_command_builder(command)
                )
            )
        await self.bot.rest.set_application_commands(
            await self.bot.rest.fetch_application(),
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
            description: Translatable = self.cast_translatable(command.description)
            builder.set_description(description.fallback)
            builder.set_description_localizations(description.translates)
        return builder

    def cast_translatable(
        self, value: Translatable | str | None, *, fallback: str | None = None
    ) -> Translatable:
        translatable: Translatable = (
            Translatable(fallback=value or fallback)
            if not isinstance(value, Translatable)
            else value
        )
        translatable.build(self.i18n_provider)
        return translatable

    def build_option(self, option: Option) -> CommandOption:
        description: Translatable = self.cast_translatable(option.description)
        choices: tuple[CommandChoice, ...] = tuple(
            CommandChoice(
                name=self.cast_translatable(choice.name).fallback, value=choice.value
            )
            for choice in option.choices
        )
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
        description: Translatable = self.cast_translatable(command.description)
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
            options=[
                self.build_sub_command(command)
                for command in sub_group.commands.values()
            ],
        )

    def get_command(
        self,
        group_name: str | None,
        subgroup_name: str | None,
        command_name: str,
    ) -> Command | None:
        commands = self.commands
        group = self.commands.get(group_name or "")
        if isinstance(group, Group):
            sub_group: SubGroup | None = group.sub_groups.get(subgroup_name or "")
            if sub_group:
                return sub_group.commands[command_name]
            return group.commands[command_name]
        command = commands[command_name]
        return command if not isinstance(command, Group) else None
