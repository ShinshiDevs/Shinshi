from typing import Sequence, Dict, List

import hikari
from hikari import impl, Snowflake, GatewayBot

from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.slash_command import SlashCommand
from shinshi.discord.workflows.builders.slash_command_builder import SlashCommandBuilder
from shinshi.discord.workflows.workflow_group import WorkflowGroup
from shinshi.i18n import I18nProvider


class WorkflowManager:
    def __init__(
        self,
        bot: GatewayBot,
        i18n_provider: I18nProvider,
        workflows: Sequence[WorkflowGroup]
    ) -> None:
        self.bot: GatewayBot = bot
        self.i18n_provider: I18nProvider = i18n_provider

        self.workflows: Sequence[WorkflowGroup] = workflows

        self.groups: Dict[Group, List[SlashCommand]] = {}
        self.sub_groups: Dict[Group, Dict[Group, List[SlashCommand]]]

        self.commands_builders: List[impl.SlashCommandBuilder] = []
        self.api_commands: List[hikari.SlashCommand] = []

    def build(self) -> None:
        for group in self.workflows:
            for workflow in group.workflows:
                workflow = workflow()
                for interactable in workflow.interactables:
                    if isinstance(interactable, SlashCommand):
                        builder: SlashCommandBuilder = SlashCommandBuilder(
                            interactable, self.i18n_provider
                        )
                        self.commands_builders.append(builder.build())

    async def sync_commands(self, application_id: Snowflake) -> None:
        for _, builder in self.commands_builders:
            app_command: hikari.SlashCommand = await builder.create(
                self.bot.rest,
                application_id,
            )
            self.api_commands.append(app_command)
