from logging import Logger, getLogger

from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
from yarl import URL

from shinshi.abc.database.idatabase_service import IDatabaseService
from shinshi.utils.env import getenv


class DatabaseService(IDatabaseService):
    def __init__(self, *models_packages: str) -> None:
        self.__logger: Logger = getLogger("shinshi.database")

        self.models_packages: tuple[str] = models_packages
        self.database_url = URL.build(
            scheme="postgres",
            user=getenv("SHINSHI_DATABASE_USER"),
            password=getenv("SHINSHI_DATABASE_PASSWORD"),
            host=getenv("SHINSHI_DATABASE_HOST"),
            port=getenv("SHINSHI_DATABASE_PORT", return_type=int),
            path=f"/{getenv('SHINSHI_DATABASE_NAME')}",
        )

    async def start(self) -> None:
        try:
            await Tortoise.init(
                db_url=str(self.database_url), modules={"models": self.models_packages}
            )
            await Tortoise.generate_schemas()
        except DBConnectionError as error:
            self.__logger.error(
                "failed to connect to database due error", exc_info=error
            )

    async def stop(self):
        await Tortoise.close_connections()
