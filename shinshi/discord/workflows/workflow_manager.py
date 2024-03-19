from typing import Sequence

from shinshi.discord.bot import Bot
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
