import os
from typing import Sequence


class Environment:
    __slots__: Sequence[str] = ()
    __root_path = os.getcwd()

    @property
    def root_path(self) -> str:
        return self.__root_path
