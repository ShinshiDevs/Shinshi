from collections.abc import Sequence
from logging import Logger, getLogger

from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
from yarl import URL

from shinshi.utils.env import getenv


class DatabaseService:
    __slots__: Sequence[str] = ("__logger", "models")

    def __init__(self, *models: str) -> None:
        self.__logger: Logger = getLogger("shinshi.database")
        self.models: tuple[str, ...] = models

    @staticmethod
    def _build_url() -> URL:
        return URL.build(
            scheme="postgres",
            user=getenv("SHINSHI_DATABASE_USER"),
            password=getenv("SHINSHI_DATABASE_PASSWORD"),
            host=getenv("SHINSHI_DATABASE_HOST"),
            port=getenv("SHINSHI_DATABASE_PORT", return_type=int),
            path=f"/{getenv('SHINSHI_DATABASE_NAME')}",
        )

    async def start(self) -> None:
        try:
            await Tortoise.init(db_url=str(self._build_url()), modules={"models": self.models})
            await Tortoise.generate_schemas()
        except DBConnectionError as error:
            self.__logger.error("failed to connect to database due error", exc_info=error)

    async def stop(self) -> None:
        await Tortoise.close_connections()
