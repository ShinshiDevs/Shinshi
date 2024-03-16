import logging
from typing import Any, Dict

from aiohttp.client import ClientSession
from aiohttp.connector import BaseConnector, TCPConnector

from shinshi import LOGGER
from shinshi.events import event_manager, StartingEvent, StoppingEvent
from shinshi.http.constants import DEFAULT_TIMEOUT
from shinshi.http.utils.orjson import orjson_serialize


class HttpPoolClient:
    def __init__(self) -> None:
        self.__logger: logging.Logger = LOGGER.getChild("http")
        self.connector: BaseConnector | None = None
        self.session: ClientSession | None = None

        event_manager.subscribe(StartingEvent, self.start)
        event_manager.subscribe(StoppingEvent, self.stop)

    async def start(self) -> None:
        self.connector: BaseConnector | None = TCPConnector()
        self.session: ClientSession | None = ClientSession(
            connector=self.connector,
            json_serialize=orjson_serialize,
            timeout=DEFAULT_TIMEOUT,
        )
        self.__logger.info("created new client session")

    async def stop(self) -> None:
        self.__logger.debug("closing session...")
        await self.session.close()
        self.__logger.debug("successfully closed session")

    async def get(self, url: str, query_parameters: Dict[str, Any] | None = None) -> Any:
        async with self.session.get(url, params=query_parameters, timeout=DEFAULT_TIMEOUT) as response:
            return await response.json()
