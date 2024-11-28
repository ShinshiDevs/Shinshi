from collections.abc import Sequence
from logging import Logger, getLogger, warning
from logging.config import dictConfig
from os import PathLike
from pathlib import Path
from os.path import basename, splitext
from typing import Any, Dict

from dotenv import load_dotenv
from yaml import CLoader, load


class ConfigurationService:
    __slots__: Sequence[str] = ("__logger", "dotenv_path", "logging_path", "configs", "stored_configs")

    def __init__(
        self,
        dotenv_path: PathLike[str] | None = None,
        logging_path: PathLike[str] | None = None,
        configs: Sequence[PathLike[str]] | None = None,
    ) -> None:
        self.__logger: Logger = getLogger("shinshi.config")
        self.dotenv_path: PathLike[str] = dotenv_path or Path(".env")
        self.logging_path: PathLike[str] = logging_path or Path("logging.yaml")

        self.configs: Sequence[PathLike[str]] = configs or []
        self.stored_configs: Dict[str, Dict[str, Any]] = {}

    async def start(self) -> None:
        for path in self.configs:
            name: str = splitext(basename(path))[0]
            config: dict[str, Any] | None = self.load_config(path)
            if config:
                self.stored_configs[name] = config
                self.__logger.debug("loaded %s config", path)
        self.__logger.info("loaded %s/%s configs", len(self.stored_configs), len(self.configs))

    async def stop(self) -> None:
        self.stored_configs.clear()

    def setup_logging(self) -> None:
        try:
            with open(self.logging_path, "rb") as stream:
                config: dict[str, str] = load(stream, Loader=CLoader)
                if not config:
                    warning("logging wasn't configured correctly because no config")
                    config = {}
        except FileNotFoundError as error:
            raise RuntimeError(f"Cannot find logging configuration {self.logging_path}") from error
        dictConfig(config)
        self.__logger.debug("configured logging successfully")

    def load_dotenv(self) -> None:
        try:
            with open(self.dotenv_path, "r", encoding="UTF-8") as stream:
                if not load_dotenv(stream=stream, override=True):  # `load_dotenv` returns bool – True if success
                    raise RuntimeError(f"Cannot load dotenv file from `{self.dotenv_path}`")
                self.__logger.debug("loaded dotenv file successfully")
        except FileNotFoundError as error:
            raise RuntimeError(f"Cannot find environment file {self.dotenv_path}") from error

    def get_config(self, name: str) -> Dict[str, Any] | None:
        return self.stored_configs.get(name)

    def load_config(self, config_path: PathLike[str]) -> Dict[str, Any] | None:
        try:
            with open(config_path, "rb") as stream:
                config: dict[str, str] = load(stream, Loader=CLoader)
                if not config:
                    self.__logger.warning("config %s is empty", config_path)
                    config = {}
                return config
        except FileNotFoundError:
            self.__logger.error("config %s is not found", config_path)
        except TypeError:
            self.__logger.error("config %s cannot be loaded due syntax error", config_path)
        return
