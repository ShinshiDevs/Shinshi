from collections.abc import Sequence

from hikari.impl import GatewayBot
from hikari.users import OwnUser


class Bot(GatewayBot):
    __slots__: Sequence[str] = ()

    @property
    def me(self) -> OwnUser:
        user: OwnUser = self.get_me()
        assert user
        return user
