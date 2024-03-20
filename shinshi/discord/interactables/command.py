from dataclasses import dataclass, field
from typing import Tuple

from hikari import Permissions, SnowflakeishOr, PartialGuild

from shinshi.discord.interactables.enum.command_type import CommandType
from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.interactables.typing.hook import HookT


@dataclass(kw_only=True)
class Command(Interactable):
    command_type: CommandType

    name: str

    default_member_permissions: Permissions = Permissions.NONE
    is_dm_enabled: bool = False
    guild: SnowflakeishOr[PartialGuild] | None = None
    is_nsfw: bool = False

    hooks: Tuple[HookT, ...] = field(default_factory=tuple)
