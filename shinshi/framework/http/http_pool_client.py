import logging
from typing import Any, Dict

from aiohttp.client import ClientSession, ClientTimeout
from aiohttp.connector import BaseConnector, TCPConnector

from shinshi import logger
from shinshi.framework.events import EventsMeta, event_listener
from shinshi.framework.events.lifetime_events import StartingEvent, StoppingEvent
from shinshi.framework.http.utils.orjson import orjson_serialize

DEFAULT_TIMEOUT: ClientTimeout = ClientTimeout(total=5)


class HttpPoolClient(metaclass=EventsMeta):
    def __init__(self) -> None:
        self.__logger: logging.Logger = logger.getChild("http")
        self.connector: BaseConnector | None = None
        self.session: ClientSession | None = None

    @event_listener(StartingEvent)
    async def start(self) -> None:
        self.connector = TCPConnector()
        self.session = ClientSession(
            connector=self.connector,
            json_serialize=orjson_serialize,
            timeout=DEFAULT_TIMEOUT,
        )
        self.__logger.info("created new client session")

    @event_listener(StoppingEvent)
    async def stop(self) -> None:
        self.__logger.debug("closing session...")
        await self.session.close()
        self.__logger.debug("successfully closed session")

    # TODO:
    #  something with this function in future for responding to functionality of bot.
    #  idk is it normal solution or not.
    async def get(self, url: str, query_parameters: Dict[str, Any] | None = None) -> Any:
        async with self.session.get(
            url, params=query_parameters, timeout=DEFAULT_TIMEOUT
        ) as response:
            return await response.json()
