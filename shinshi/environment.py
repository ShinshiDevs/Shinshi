import os
from typing import Sequence


class Environment:
    __slots__: Sequence[str] = ()
    _root_path: str = os.getcwd()

    @property
    def root_path(self) -> str:
        return self._root_path
