from logging import Logger, getLogger, warning
from logging.config import dictConfig
from os import PathLike

from dotenv import load_dotenv
from yaml import CLoader, load

from shinshi.abc.config.iconfiguration_service import IConfigurationService


class ConfigurationService(IConfigurationService):
    def __init__(
        self,
        dotenv_path: PathLike[str] = ".env",
        logging_path: PathLike[str] = "logging.yaml",
    ) -> None:
        self.__logger: Logger = getLogger("shinshi.config")
        self.dotenv_path: PathLike[str] = dotenv_path
        self.logging_path: PathLike[str] = logging_path

    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...

    def configure_logging(self) -> None:
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
                if not load_dotenv(
                    stream=stream, override=True
                ):  # `load_dotenv` returns bool – True if success
                    raise RuntimeError(f"Cannot load dotenv file from `{self.dotenv_path}`")
                self.__logger.debug("loaded dotenv file successfully")
        except FileNotFoundError as error:
            raise RuntimeError(f"Cannot find environment file {self.dotenv_path}") from error
