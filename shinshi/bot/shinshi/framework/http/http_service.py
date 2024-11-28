from logging import Logger, getLogger
from typing import Sequence

import orjson
from aiohttp import ClientSession, TCPConnector


class HTTPService:
    __slots__: Sequence[str] = ("__logger", "client_session", "connector")

    def __init__(self) -> None:
        self.__logger: Logger = getLogger("shinshi.http")

        self.client_session: ClientSession | None = None
        self.connector: TCPConnector | None = None

    async def start(self) -> None:
        self.connector = TCPConnector(enable_cleanup_closed=True)
        self.client_session = ClientSession(
            connector=self.connector,
            json_serialize=orjson.dumps,  # type: ignore
        )
        self.__logger.debug("created client session with connector")

    async def stop(self) -> None:
        if self.client_session is not None:
            await self.client_session.close()
            self.connector = None
            self.client_session = None
            self.__logger.debug("closed and removed client session with connector")
