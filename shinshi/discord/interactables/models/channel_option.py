from dataclasses import dataclass
from typing import Sequence

from hikari import ChannelType

from shinshi.discord.interactables.models.option import Option


@dataclass
class ChannelOption(Option):
    channel_types: Sequence[ChannelType] | None = None
