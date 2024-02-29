from typing import Protocol, Awaitable


class IntegrationInterface(Protocol):
    def start(self) -> Awaitable[None]:
        raise NotImplementedError

    def stop(self) -> Awaitable[None]:
        raise NotImplementedError
