from typing import Protocol, Awaitable


class IStartable(Protocol):
    def start(self) -> Awaitable[None]:
        raise NotImplementedError

    def stop(self) -> Awaitable[None]:
        raise NotImplementedError
