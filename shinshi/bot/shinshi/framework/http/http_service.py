import orjson
from aiohttp import ClientSession, TCPConnector

from shinshi.abc.http.ihttp_service import IHTTPService
from shinshi.framework.types.singleton import Singleton


class HTTPService(Singleton, IHTTPService):
    def __init__(self) -> None:
        self.client_session: ClientSession | None = None
        self.connector: TCPConnector | None = None

    async def start(self) -> None:
        self.connector = TCPConnector(enable_cleanup_closed=True)
        self.client_session = ClientSession(
            connector=self.connector,
            json_serialize=orjson.dumps,
        )

    async def stop(self) -> None:
        await self.connector.close()
        await self.client_session.close()

        self.connector = None
        self.client_session = None
