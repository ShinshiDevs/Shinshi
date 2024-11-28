from __future__ import annotations

from typing import TYPE_CHECKING
from shinshi.abc.i18n.ii18n_provider import II18nProvider
from logging import getLogger, Logger
from collections import defaultdict

from aurum.commands import impl
from aurum.commands.base_command import BaseCommand
from hikari.api import special_endpoints as api
from hikari.applications import Application
from hikari.events.interaction_events import InteractionCreateEvent
from hikari.snowflakes import SnowflakeishOr
from hikari.guilds import PartialGuild
from hikari.interactions import CommandInteraction

from shinshi.framework.bot.bot import Bot
from shinshi.framework.commands.command_builder import CommandBuilder
from shinshi.framework.context.context import Context

if TYPE_CHECKING:
    from aurum.commands.types import CommandMapping


class CommandHandler(impl.CommandHandler):
    def __init__(self, bot: Bot, i18n_provider: II18nProvider, *, sync_commands: bool = False) -> None:
        self.__logger: Logger = getLogger("shinshi.commands")
        self.__application: Application | None = None

        self.bot: Bot = bot
        self.i18n_provider: II18nProvider = i18n_provider
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.on_command_interaction)

        self.sync_commands_flag: bool = sync_commands

        self.commands: dict[str, BaseCommand] = {}
        self.global_commands: CommandMapping = {}
        self.guild_commands: dict[SnowflakeishOr[PartialGuild], CommandMapping] = defaultdict()

        self._builder: CommandBuilder = CommandBuilder(i18n_provider)
        self._commands_builders: dict[BaseCommand, api.CommandBuilder] = {}

    def create_context(self, interaction: CommandInteraction) -> Context:
        return Context(
            interaction=interaction,
            bot=self.bot,
            locale=self.i18n_provider.get_default_locale(),  # TODO: locale recognize
        )

    async def start(self) -> None:
        self.__logger.debug("starting")
        if self.sync_commands_flag is True:
            self.__logger.debug("syncing commands")
            self.__application = await self.bot.rest.fetch_application()
            self._commands_builders = self._builder.build_commands(self.bot, self.commands)
            await self.sync_commands()
