from collections.abc import Sequence
from importlib import import_module
from logging import Logger, getLogger

from aurum import LocalizationProviderInterface, SyncCommandsFlag
from aurum.client import Client as AurumClient
from aurum.commands.app_command import AppCommand
from hikari.traits import GatewayBotAware

from shinshi.types.events import EventCallback
from shinshi.managers import ExtensionManager


class Client(AurumClient):
    __slots__: Sequence[str] = ("extensions",)

    def __init__(
        self,
        bot: GatewayBotAware,
        *,
        l10n: LocalizationProviderInterface | None = None,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
        ignore_l10n: bool = False,
        ignore_unknown_interactions: bool = False,
    ) -> None:
        super().__init__(
            bot,
            l10n=l10n,
            sync_commands=sync_commands,
            ignore_l10n=ignore_l10n,
            ignore_unknown_interactions=ignore_unknown_interactions,
        )
        self.__logger: Logger = getLogger(__name__)

        self.extensions: ExtensionManager = ExtensionManager(self)

    def load_events(self, module_name: str) -> None:
        module = import_module(module_name)
        for event in module.__all__:
            event: EventCallback = getattr(module, event)
            self.bot.event_manager.subscribe(getattr(event, "__event_type"), event)

    def run(self, **kwargs) -> None:
        self.__logger.info("starting")
        self.bot.run(**kwargs)

    def add_command(self, command: AppCommand) -> None:
        self.commands.commands[command.name] = command
