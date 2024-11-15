from abc import abstractmethod
from typing import Protocol
from typing_extensions import runtime_checkable


@runtime_checkable
class IService(Protocol):
    async def start(self) -> None: ...

    async def stop(self) -> None: ...
