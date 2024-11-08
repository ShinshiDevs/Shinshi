from collections.abc import Sequence
from logging import Logger, getLogger, warning
from logging.config import dictConfig
from os import PathLike
from posixpath import basename, splitext

from dotenv import load_dotenv
from yaml import CLoader, load

from shinshi.abc.config.iconfiguration_service import IConfigurationService
from shinshi.framework.types.singleton import Singleton


class ConfigurationService(Singleton, IConfigurationService):
    __slots__: Sequence[str] = ("__logger", "dotenv_path", "logging_path", "configs")

    def __init__(
        self,
        dotenv_path: PathLike[str] = ".env",
        logging_path: PathLike[str] = "logging.yaml",
        configs: Sequence[PathLike[str]] | None = None,
    ) -> None:
        self.__logger: Logger = getLogger("shinshi.config")
        self.dotenv_path: PathLike[str] = dotenv_path
        self.logging_path: PathLike[str] = logging_path

        self.configs: Sequence[PathLike[str]] = configs or []
        self.stored_configs: dict[str, dict] = {}

    async def start(self) -> None:
        for path in self.configs:
            name: str = splitext(basename(path))[0]
            config: dict = self.load_config(path)
            if config:
                self.stored_configs[name] = config
                self.__logger.debug("loaded %s config", path)
        self.__logger.info(
            "loaded %s/%s configs", len(self.stored_configs), len(self.configs)
        )

    async def stop(self) -> None:
        self.stored_configs.clear()

    def get_config(self, name: str) -> dict | None:
        return self.stored_configs.get(name)

    def configure_logging(self) -> None:
        try:
            with open(self.logging_path, "rb") as stream:
                config: dict[str, str] = load(stream, Loader=CLoader)
                if not config:
                    warning("logging wasn't configured correctly because no config")
                    config = {}
        except FileNotFoundError as error:
            raise RuntimeError(
                f"Cannot find logging configuration {self.logging_path}"
            ) from error
        dictConfig(config)
        self.__logger.debug("configured logging successfully")

    def load_dotenv(self) -> None:
        try:
            with open(self.dotenv_path, "r", encoding="UTF-8") as stream:
                if not load_dotenv(
                    stream=stream, override=True
                ):  # `load_dotenv` returns bool – True if success
                    raise RuntimeError(
                        f"Cannot load dotenv file from `{self.dotenv_path}`"
                    )
                self.__logger.debug("loaded dotenv file successfully")
        except FileNotFoundError as error:
            raise RuntimeError(
                f"Cannot find environment file {self.dotenv_path}"
            ) from error

    def load_config(self, config_path: PathLike[str]) -> dict | None:
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
            self.__logger.error(
                "config %s cannot be loaded due syntax error", config_path
            )
        return
