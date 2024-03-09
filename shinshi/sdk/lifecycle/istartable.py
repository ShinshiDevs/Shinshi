from typing import Protocol


class IStartable(Protocol):
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...
