from typing import Protocol

from shinshi.framework.bot.bot import Bot


class IBotService(Protocol):
    @property
    def bot(self) -> Bot: ...
