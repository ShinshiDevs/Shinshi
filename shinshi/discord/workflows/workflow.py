from typing import Protocol


class Workflow(Protocol):
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...
