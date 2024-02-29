import asyncio
import sys
from asyncio import AbstractEventLoop, Task
from logging import Logger
from os import environ
from typing import Sequence

from hikari.intents import Intents
from hikari.impl import HTTPSettings
from kanata.decorators import injectable
from orjson import loads, dumps

from shinshi.framework.discord.sdk import BotServiceInterface
from shinshi.framework.dotenv.utils import get_log_level
from shinshi.framework.logging import LoggerFactory
from .bot import BaseBot

REQUIRED_INTENTS: Intents = (
    Intents.GUILDS
    | Intents.GUILD_EMOJIS
    | Intents.GUILD_MESSAGES
    | Intents.GUILD_MODERATION
)


@injectable(BotServiceInterface)
class BotService(BotServiceInterface):
    __slots__: Sequence[str] = (
        "loop",
        "log_level",
        "logger",
        "__bot",
        "bot_task",
        "bot_kwargs",
        "asyncio_debug",
        "coroutine_tracking_depth",
    )

    def __init__(self):
        super().__init__()
        self.loop: AbstractEventLoop = asyncio.get_event_loop()
        self.logger: Logger = LoggerFactory.create(BotService)

        self.__bot: BaseBot = self.__create()
        self.bot_task: Task | None = None
        self.bot_kwargs = {}

    async def start(self) -> None:
        if self.bot_task is not None:
            raise RuntimeError("The bot is running already.")
        self.loop.set_debug(self.asyncio_debug)
        try:
            sys.set_coroutine_origin_tracking_depth(self.coroutine_tracking_depth)
        except AttributeError:
            self.logger.warning(
                "cannot set coroutine tracking depth for sys, "
                "no functionality exists for this"
            )
        self.bot_task = self.loop.create_task(self.bot.start(**self.bot_kwargs))

    async def stop(self) -> None:
        if self.bot_task is None:
            return
        await self.bot.close()
        await self.bot_task
        self.bot_task = None

    @property
    def bot(self) -> BaseBot:
        return self.__bot

    @staticmethod
    def __create() -> BaseBot | None:
        return BaseBot(
            token=environ.get("SHINSHI_DISCORD_TOKEN"),
            banner=None,
            intents=REQUIRED_INTENTS,
            logs=get_log_level(),
            loads=loads,
            dumps=dumps,
            http_settings=HTTPSettings(enable_cleanup_closed=False),
        )
