from typing import Sequence

from hikari.intents import Intents

__all__: Sequence[str] = (
    "intents",
)

intents: Intents = (
    Intents.GUILDS
    | Intents.GUILD_EMOJIS
    | Intents.GUILD_MESSAGES
    | Intents.GUILD_MODERATION
)
