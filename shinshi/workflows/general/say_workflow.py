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
from hikari.channels import ChannelType
from hikari.commands import OptionType
from hikari.errors import ForbiddenError, InternalServerError, NotFoundError
from hikari.interactions import InteractionChannel
from hikari.messages import Attachment
from hikari.permissions import Permissions
from hikari.webhooks import ExecutableWebhook

from shinshi.discord.interactables.options import ChannelOption, Option, StringOption
from shinshi.discord.interaction.interaction_context import InteractionContext
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows import Workflow
from shinshi.discord.workflows.decorators import command
from shinshi.workflows.general.exceptions import (
    InsufficientArgumentsException,
    WebhookCreationException,
    WebhookExecutionException,
)


# TODO: FIX, not working command
class SayWorkflow(Workflow):
    @command(
        description=Translatable("commands.say.description"),
        is_defer=True,
        options=(
            StringOption(
                type=OptionType.STRING,
                name="content",
                description=Translatable("commands.say.arguments.content.description"),
                is_required=False,
                max_length=2000,
            ),
            Option(
                type=OptionType.ATTACHMENT,
                name="attachment",
                description=Translatable(
                    "command.say.arguments.attachment.description"
                ),
                is_required=False,
            ),
            ChannelOption(
                type=OptionType.CHANNEL,
                name="channel",
                description=Translatable("command.say.arguments.channel.description"),
                is_required=False,
                channel_types=(ChannelType.GUILD_TEXT,),
            ),
        ),
    )
    async def say(
        self,
        context: InteractionContext,
        content: str | None = None,
        attachment: Attachment | None = None,
        channel: InteractionChannel | None = None,
    ) -> None:
        if content is None and attachment is None:
            raise InsufficientArgumentsException(context)
        if channel:
            if not Permissions.SEND_MESSAGES & channel.permissions:
                raise WebhookExecutionException(context)
        try:
            webhook: ExecutableWebhook = await context.bot.rest.create_webhook(
                channel=channel or context.interaction.channel_id,
                name=context.interaction.member.id,
                reason=(
                    f"Created webhook for @{context.interaction.member.username}"
                    f" (ID: {context.interaction.member.id})"
                ),
            )
        except (ForbiddenError, NotFoundError, InternalServerError):
            raise WebhookCreationException(context)
        try:
            try:
                webhook: ExecutableWebhook | None = None
                if (
                    webhooks := await context.bot.cache.get_channel_webhooks(
                        context.interaction.channel_id
                    )
                ) is not None:
                    for channel_webhook in webhooks:
                        if str(context.interaction.member.id) == str(channel_webhook):
                            webhook = channel_webhook
                            break
                else:
                    webhook = await context.bot.rest.create_webhook(
                        channel=channel or context.interaction.channel_id,
                        name=context.member.id,
                        reason=(
                            f"Created webhook for @{context.interaction.member.username}"
                            f" (ID: {context.interaction.member.id})"
                        ),
                    )
            except (ForbiddenError, NotFoundError, InternalServerError):
                raise WebhookCreationException(context)
            await webhook.execute(
                content=content,
                attachment=attachment,
                username=context.interaction.member.display_name,
                avatar_url=context.interaction.member.display_avatar_url,
            )
        except ValueError:
            raise WebhookExecutionException(context)
