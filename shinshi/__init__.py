from typing import Sequence

from hikari.intents import Intents

import extensions

__all__: Sequence[str] = (
    "intents",
    "workflows"
)

intents: Intents = (
    Intents.GUILDS
    | Intents.GUILD_EMOJIS
    | Intents.GUILD_MESSAGES
    | Intents.GUILD_MODERATION
)

workflows: Sequence[...] = (
    # General
    extensions.general.InfoWorkflow,
)
