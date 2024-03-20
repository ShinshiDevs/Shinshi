from dataclasses import dataclass

from hikari import Permissions


@dataclass(kw_only=True)
class Group:
    name: str

    default_member_permissions: Permissions = Permissions.NONE
    is_dm_enabled: bool = False
    is_nsfw: bool = False
