import logging
from os import environ

from kanata.decorators import injectable

from shinshi.framework.discord.sdk import BotServiceInterface
from shinshi.sdk.integration import IntegrationInterface
from shinshi.framework.logging import LoggerFactory


@injectable(IntegrationInterface)
class DiscordIntegration(IntegrationInterface):
    def __init__(
        self,
        bot: BotServiceInterface,
    ) -> None:
        super().__init__()
        self.bot: BotServiceInterface = bot
        self.logger: logging.Logger = LoggerFactory.create(DiscordIntegration)

    async def start(self) -> None:
        self.logger.debug("Starting Discord integration...")
        if environ.get("SHINSHI_IS_HIKARI_TRACE_ENABLED").upper() == "TRUE":
            rest_logger: logging.Logger = logging.getLogger("hikari.rest")
            rest_logger.setLevel("TRACE_HIKARI")
        await self.bot.start()
        self.logger.info("Discord integration started")

    async def stop(self) -> None:
        self.logger.debug("Stopping Discord integration...")
        await self.bot.stop()
        self.logger.info("Discord integration stopped")
