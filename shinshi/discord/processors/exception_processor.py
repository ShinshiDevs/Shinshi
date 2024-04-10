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
import os
import traceback
from datetime import datetime

from hikari.embeds import Embed
from hikari.messages import Message
from hikari.webhooks import ExecutableWebhook

from shinshi.discord.exceptions.interaction_exception import InteractionException
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.utils.string import get_codeblock


class ExceptionProcessor:
    async def send_report(
        self, exception: Exception, context: InteractionContext
    ) -> Message | None:
        traceback_message = (
            "..."
            + "".join(
                traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                )
            )[-997:]
        )
        webhook: ExecutableWebhook = await self.bot.cache.get_webhook(
            os.environ.get("SHINSHI_ERRORS_WEBHOOK_ID")
        )
        embed = Embed(
            title="Report",
            description=(
                f"{type(exception).__qualname__} occurred while `{context.interactable}` "
                f"by {context.interaction.user.username} (ID: {context.interaction.user.id})"
            ),
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(name="Traceback", value=get_codeblock("py", traceback_message))
        if guild := context.interaction.get_guild():
            embed.set_footer(text=f"Shard ID: #{guild.shard_id}")
        return await webhook.execute(embed=embed)

    async def proceed_exception(
        self, context: InteractionContext, exception: Exception
    ) -> None:
        if isinstance(exception, InteractionException):
            try:
                return await exception.callback()
            except Exception as exception:
                self.__logger.error(
                    "Cannot handle exception, because of another exception",
                    exc_info=exception,
                )
        else:
            await self.send_report(exception, context)
            return await Exception(context).callback()
