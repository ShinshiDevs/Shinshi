from abc import abstractmethod
from typing import Protocol


class IService(Protocol):
    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
