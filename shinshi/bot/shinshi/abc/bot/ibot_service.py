from aurum.client import Client
from hikari.traits import GatewayBotAware

from shinshi.abc.services.iservice import IService


class IBotService(IService):
    @property
    def bot(self) -> GatewayBotAware: ...

    @property
    def client(self) -> Client: ...
