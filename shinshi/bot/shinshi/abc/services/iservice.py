from abc import abstractmethod
from typing import Protocol
from typing_extensions import runtime_checkable


@runtime_checkable
class IService(Protocol):
    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
