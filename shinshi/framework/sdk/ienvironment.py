from typing import Protocol


class IEnvironment(Protocol):
    @property
    def root_path(self) -> str:
        ...
