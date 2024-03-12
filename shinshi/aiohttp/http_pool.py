import asyncio
import logging

from aiohttp.client import ClientResponse, ClientSession
from aiohttp.connector import TCPConnector
from aiohttp.typedefs import StrOrURL

from shinshi.sdk.lifecycle import IStartable
from shinshi.utils.orjson import orjson_serialize


class HttpPool(IStartable):
    connector: TCPConnector | None = None
    session: ClientSession | None = None

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.__loop: asyncio.AbstractEventLoop = loop
        self.__logger: logging.Logger = logging.getLogger("shinshi.http_pool")

    async def start(self) -> None:
        self.connector = TCPConnector(loop=self.__loop)
        self.session = ClientSession(
            loop=self.__loop,
            connector=self.connector,
            json_serialize=orjson_serialize,
        )
        self.__logger.debug("Created new client session")

    async def stop(self) -> None:
        await self.session.close()
        await self.connector.close()
        self.__logger.debug("Stopped")

    async def request(
        self, method: str, url: StrOrURL, **kwargs
    ) -> ClientResponse | None:
        response: ClientResponse = await self.session.request(method, url, **kwargs)
        if response.status not in (200, 201):
            self.__logger.warning(f"Invalid response with code {response.status}")
            return None
        return response
