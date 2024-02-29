from typing import Awaitable, Protocol


class BotServiceInterface(Protocol):
    def start(self) -> Awaitable[None]:
        ...

    def stop(self) -> Awaitable[None]:
        ...
