from os import PathLike

from shinshi.abc.services.iservice import IService


class IConfigurationService(IService):
    def setup_logging(self) -> None: ...

    def load_dotenv(self) -> None: ...

    def get_config(self, name: str) -> dict | None: ...

    def load_config(self, config_path: PathLike[str]) -> dict | None: ...
