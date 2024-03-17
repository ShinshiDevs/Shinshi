from hikari import GatewayBot

from shinshi.events import EventsMeta


class BotMeta(
    type(GatewayBot),
    EventsMeta
):
    ...
