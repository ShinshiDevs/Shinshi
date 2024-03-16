from hikari import GatewayBot

from shinshi.events import RegisterEventsMeta


class BotMeta(
    type(GatewayBot),
    RegisterEventsMeta
):
    ...
