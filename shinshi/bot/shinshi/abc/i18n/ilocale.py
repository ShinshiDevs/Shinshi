from abc import abstractmethod
from typing import Any, List, Protocol, Dict


class ILocale(Protocol):
    name: str
    data: Dict[str, str]

    @abstractmethod
    def get(self, key: str, formatting: Dict[str, Any] | None = None) -> str: ...

    @abstractmethod
    def get_list(self, key: str, *formatting: Dict[str, Any]) -> List[str]: ...
