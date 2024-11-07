import time

from hikari import GatewayBot


class Bot(GatewayBot):
    def __init__(self, *args, **kwargs) -> None:
        self.uptime: int | None = None
        super().__init__(*args, **kwargs)

    async def start(self, *args, **kwargs) -> None:
        self.uptime = time.time()
        return await super().start(*args, **kwargs)

    async def close(self) -> None:
        self.uptime = None
        return await super().close()
