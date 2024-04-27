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
from collections.abc import Sequence
from datetime import datetime, timedelta

from cachetools import TTLCache
from hikari.snowflakes import Snowflake

from shinshi import IMAGES_DIR
from shinshi.discord.interactables.hooks import Hook, HookResult
from shinshi.discord.interaction import InteractionContext
from shinshi.ext.hooks.cooldown.bucket import BucketType
from shinshi.utils.string import format_datetime


class Cooldown:
    __slots__: Sequence[str] = ("period", "bucket", "cache")

    def __init__(
        self, period: timedelta, *, bucket: BucketType = BucketType.USER
    ) -> None:
        self.period = period
        self.bucket = bucket
        self.cache: TTLCache[Snowflake | tuple[Snowflake, ...], datetime] = TTLCache(
            maxsize=1000, ttl=period.total_seconds()
        )

    async def delete_after(self, context: InteractionContext) -> None:
        await asyncio.sleep(self.period.total_seconds())
        await context.delete_response()

    async def callback(self, context: InteractionContext) -> HookResult:
        bucket: Snowflake | tuple[Snowflake, ...] = self.bucket(context)
        if (retry_after := self.cache.get(bucket)) is None:
            self.cache[bucket] = datetime.now() + self.period
            return HookResult(stop=False)
        else:
            await asyncio.gather(
                context.send_warning(
                    content=context.i18n.get("exceptions.cooldown_warning.content"),
                    description=context.i18n.get(
                        "exceptions.cooldown_warning.description",
                        {"retry_after": format_datetime(retry_after, "R")},
                    ),
                    icon=IMAGES_DIR / "cooldown_warning.webp",
                ),
                self.delete_after(context),
            )
            return HookResult(stop=True)

    @property
    def hook(self) -> Hook:
        return Hook(callback=self.callback)
