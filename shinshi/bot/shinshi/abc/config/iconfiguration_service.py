from os import PathLike
from typing import Protocol, TypeVar

from shinshi.abc.services.iservice import IService

T = TypeVar("T")


class IConfigurationService(IService, Protocol):
    def setup_logging(self) -> None: ...

    def load_dotenv(self) -> None: ...

    def get_config(self, name: str) -> T | None: ...

    def load_config(self, config_path: PathLike[str]) -> T | None: ...
