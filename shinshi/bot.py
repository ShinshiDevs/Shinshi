from hikari.impl import GatewayBot
from hikari.users import OwnUser


class Bot(GatewayBot):
    @property
    def me(self) -> OwnUser:
        return self.get_me()
