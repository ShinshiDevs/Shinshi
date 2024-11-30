from abc import abstractmethod
from typing import Any, Protocol


class ILocale(Protocol):
    name: str
    data: dict[str, str]

    @abstractmethod
    def get(self, key: str, formatting: dict[str, Any] | None = None) -> str: ...

    @abstractmethod
    def get_list(self, key: str, *formatting: dict[str, Any]) -> list[str]: ...
