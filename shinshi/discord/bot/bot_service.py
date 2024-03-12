import logging
from asyncio import AbstractEventLoop, Task
from typing import Sequence

from shinshi.discord.bot import DiscordBot
from shinshi.logging import LoggerFactory
from shinshi.sdk.lifecycle import IStartable
from shinshi.utils.dotenv import dotenv_get_boolean


class BotService(IStartable):
    __slots__: Sequence[str] = ("__logger", "__loop", "bot", "bot_task")

    def __init__(
        self,
        loop: AbstractEventLoop,
        bot: DiscordBot,
    ) -> None:
        self.__logger: logging.Logger = LoggerFactory.create(BotService)
        self.__loop: AbstractEventLoop = loop

        self.bot: DiscordBot = bot
        self.bot_task: Task | None = None

    async def start(self) -> None:
        if dotenv_get_boolean("SHINSHI_IS_HIKARI_NETWORK_TRACE_ENABLED") is True:
            rest_logger: logging.Logger = logging.getLogger("hikari.rest")
            rest_logger.setLevel("TRACE_HIKARI")
        if self.bot_task is not None:
            raise RuntimeError("The bot is running already.")
        self.bot_task = self.__loop.create_task(self.bot.start())

    async def stop(self) -> None:
        if self.bot_task is None:
            return
        await self.bot.close()
        await self.bot_task
        self.bot_task = None
