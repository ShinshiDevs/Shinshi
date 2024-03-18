from typing import Tuple, Callable, Awaitable, Any

from hikari import Permissions

from shinshi.discord.context.typing import ContextT
from shinshi.discord.interactables.enum.command_type import CommandType
from shinshi.discord.interactables.models.option import Option
from shinshi.discord.interactables.models.translatable import Translatable
from shinshi.discord.interactables.slash_command import SlashCommand
from shinshi.discord.interactables.typing.hook import HookT


def slash_command(
    name: str,
    description: Translatable,
    options: Tuple[Option, ...] | None = None,
    hooks: Tuple[HookT, ...] | None = None,
    default_member_permissions: Permissions | None = None,
    dm_enabled: bool | None = None,
    is_nsfw: bool | None = None,
) -> Callable[[Callable[[ContextT, ...], Awaitable[Any]]], SlashCommand]:
    def decorator(func: Callable[[ContextT, ...], Awaitable[Any]]) -> SlashCommand:
        return SlashCommand(
            command_type=CommandType.SLASH,
            callback=func,
            name=name or func.__name__,
            description=description,
            options=options,
            hooks=hooks,
            default_member_permissions=default_member_permissions,
            dm_enabled=dm_enabled,
            is_nsfw=is_nsfw
        )

    return decorator
