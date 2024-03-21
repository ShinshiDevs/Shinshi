from typing import Tuple, Callable

from hikari import Permissions

from shinshi.discord.interactables.enum.command_type import CommandType
from shinshi.discord.interactables.models.option import Option
from shinshi.discord.interactables.slash_command import SlashCommand
from shinshi.discord.interactables.typing.hook import HookT
from shinshi.discord.interactables.typing.interactable_callback import InteractableCallbackT
from shinshi.discord.models.translatable import Translatable


def slash_command(
    name: str | None = None,
    description: Translatable | None = None,
    options: Tuple[Option, ...] | None = None,
    hooks: Tuple[HookT, ...] | None = None,
    default_member_permissions: Permissions | None = None,
    dm_enabled: bool | None = None,
    is_nsfw: bool | None = None,
) -> Callable[[InteractableCallbackT], SlashCommand]:
    def decorator(func: InteractableCallbackT) -> SlashCommand:
        return SlashCommand(
            command_type=CommandType.SLASH,
            callback=func,
            name=name or func.__name__,
            description=description,
            options=options,
            hooks=hooks,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=dm_enabled,
            is_nsfw=is_nsfw
        )

    return decorator
