from hikari.users import OwnUser
from hikari.impl import GatewayBot


class Bot(GatewayBot):
    @property
    def me(self) -> OwnUser:
        return self.get_me()
