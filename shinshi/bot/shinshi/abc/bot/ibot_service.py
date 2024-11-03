from typing import Protocol

from aurum.client import Client
from hikari.traits import GatewayBotAware

from shinshi.abc.services.iservice import IService


class IBotService(IService, Protocol):
    @property
    def bot(self) -> GatewayBotAware:
        ...

    @property
    def client(self) -> Client:
        ...
