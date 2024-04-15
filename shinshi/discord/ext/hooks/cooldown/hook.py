# Copyright (C) 2024 Shinshi Developers Team
#
# This file is part of Shinshi.
#
# Shinshi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinshi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Shinshi.  If not, see <https://www.gnu.org/licenses/>.
import asyncio
from datetime import datetime, timedelta

from cachetools import TTLCache
from hikari.snowflakes import Snowflake

from shinshi.discord.ext.hooks.cooldown.bucket import BucketType
from shinshi.discord.interactables.hooks import HookResult, HookT
from shinshi.discord.interaction import InteractionContext
from shinshi.utils.string import format_datetime


def cooldown(period: timedelta, *, _bucket: BucketType = BucketType.USER) -> HookT:
    """Creates a cooldown hook using TTLCache.

    This hook prevents the command from being used again within a certain period of time.

    Args:
        period (timedelta): The amount of time before the command can be used again.
        _bucket (BucketType, optional): The bucket type for ratelimiting. Defaults to BucketType.USER.
    Returns:
        Callable: A hook function to be used before command execution.
    """
    cache: TTLCache[Snowflake | tuple[Snowflake, ...], datetime] = TTLCache(
        maxsize=1000, ttl=period.total_seconds()
    )

    async def delete_after(context: InteractionContext) -> None:
        await asyncio.sleep(period.total_seconds())
        await context.delete_response()

    async def hook(context: InteractionContext) -> HookResult:
        bucket: Snowflake | tuple[Snowflake, ...] = _bucket(context)
        if (retry_after := cache.get(bucket)) is None:
            cache[bucket] = datetime.now() + period
            return HookResult(stop=False)
        else:
            asyncio.gather(
                context.send_warning(
                    context.i18n.get(
                        "exceptions.cooldown_error",
                        {"retry_after": format_datetime(retry_after, "R")},
                    )
                ),
                delete_after(context),
            )
            return HookResult(stop=True)

    return hook
