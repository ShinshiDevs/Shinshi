from dataclasses import dataclass, field
from typing import Tuple

from hikari import Permissions

from shinshi.discord.interactables.enum.command_type import CommandType
from shinshi.discord.interactables.interactable import Interactable
from shinshi.discord.interactables.typing.hook import HookT


@dataclass(kw_only=True)
class Command(Interactable):
    command_type: CommandType

    name: str

    default_member_permissions: Permissions = Permissions.NONE
    dm_enabled: bool = False
    is_nsfw: bool = False

    hooks: Tuple[HookT, ...] = field(default_factory=tuple)
