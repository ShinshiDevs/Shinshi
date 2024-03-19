from typing import Sequence, List, Dict, Any

import hikari
from hikari import Locale, CommandOption, CommandChoice
from hikari.impl import SlashCommandBuilder

from shinshi.discord.bot import Bot
from shinshi.discord.interactables.command import Command
from shinshi.discord.interactables.models.channel_option import ChannelOption
from shinshi.discord.interactables.models.number_option import NumberOption
from shinshi.discord.interactables.models.string_option import StringOption
from shinshi.discord.interactables.models.translatable import Translatable
from shinshi.discord.interactables.slash_command import SlashCommand
from shinshi.discord.workflows.workflow_base import WorkflowBase
from shinshi.discord.workflows.workflow_group import WorkflowGroup
from shinshi.i18n import I18nProvider


class WorkflowManager:
    def __init__(
        self,
        bot: Bot,
        i18n_provider: I18nProvider,
        workflows: Sequence[WorkflowBase, WorkflowGroup]
    ) -> None:
        self.bot: Bot = bot
        self.i18n_provider: I18nProvider = i18n_provider

        self.workflows: Sequence[WorkflowBase, WorkflowGroup] = workflows

        self.commands_builders: Dict[Command: SlashCommandBuilder] = {}
        self.commands: Dict[Command, hikari.SlashCommand] = {}

    def build_workflow(self, workflow: WorkflowBase) -> None:
        for interactable in workflow.interactables:
            if isinstance(interactable, SlashCommand):
                self.commands_builders[interactable] = self.get_slash_command_builder(interactable)

    async def start(self) -> None:
        for workflow in self.workflows:
            if isinstance(workflow, WorkflowGroup):
                for sub_workflow in workflow.workflows:
                    self.build_workflow(sub_workflow)
                continue
            self.build_workflow(workflow)

    async def sync(self) -> None:
        for command, builder in self.commands_builders.items():
            builder.create(
                self.bot.rest,
                self.bot,
                guild=command.guild,
            )

    def get_slash_command_builder(self, command: SlashCommand) -> SlashCommandBuilder:
        description: Dict[Locale, str] = (
            command.description.translate(self.i18n_provider)
        )
        builder: SlashCommandBuilder = SlashCommandBuilder(
            name=command.name,
            description=description[Locale.EN_US],
            description_localizations=description,
            default_member_permissions=command.default_member_permissions,
            is_dm_enabled=command.dm_enabled,
            is_nsfw=command.is_nsfw,
        )
        for option in command.options:
            option_kwargs: Dict[str, Any] = {}
            option_descriptions: Dict[Locale, str] = (
                option.description.translate(self.i18n_provider)
            )
            if isinstance(option, StringOption):
                option_kwargs["max_length"] = option.max_length
                option_kwargs["min_length"] = option.min_length
            if isinstance(option, NumberOption):
                option_kwargs["max_value"] = option.max_value
                option_kwargs["min_value"] = option.min_value
            if isinstance(option, ChannelOption):
                option_kwargs["channel_types"] = option.channel_types

            option_choices: List[CommandChoice] = []
            for choice in option.choices:
                choice_name: Dict[Locale, str] | str = (
                    choice.name.translate(self.i18n_provider)
                    if isinstance(choice.name, Translatable)
                    else choice.name
                )
                option_choices.append(
                    CommandChoice(
                        name=(
                            choice_name[Locale.EN_US]
                            if isinstance(choice_name, dict) else choice.name
                        ),
                        name_localizations=(
                            choice_name if isinstance(choice_name, dict) else None
                        ),
                        value=choice.value,
                    )
                )

            command_option: CommandOption = CommandOption(
                type=option.type,
                name=option.name,
                description=option_descriptions[Locale.EN_US],
                description_localizations=option_descriptions,
                is_required=option.required,
                autocomplete=option.is_autocomplete,
                choices=option_choices,
                **option_kwargs
            )
            builder.add_option(command_option)
        return builder
