from typing import List

from hikari import GatewayBot, StartingEvent

from shinshi.discord.workflows.builders.workflow_builder import WorkflowBuilder
from shinshi.discord.workflows.data.workflow_repository import WorkflowRepository


class WorkflowManager:
    def __init__(
        self, bot: GatewayBot, repositories: List[WorkflowRepository]
    ) -> None:
        self.__repositories: List[WorkflowRepository] = repositories
        self.__builder: WorkflowBuilder = WorkflowBuilder()

        self.bot = bot
        self.bot.event_manager.subscribe(StartingEvent, self.__start)

        self.workflows = []

    async def __start(self, _: StartingEvent) -> None:
        ...
