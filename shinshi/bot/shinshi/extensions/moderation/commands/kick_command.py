import contextlib
from datetime import UTC, datetime
from logging import getLogger

from aurum.commands import SlashCommand
from aurum.l10n import Localized
from aurum.option import Option
from hikari.commands import OptionType
from hikari.embeds import Embed
from hikari.errors import BadRequestError, ForbiddenError, NotFoundError
from hikari.guilds import GatewayGuild, Member
from hikari.permissions import Permissions

from shinshi.abc.config.iconfiguration_service import IConfigurationService
from shinshi.enums.colour import Colour
from shinshi.extensions.moderation.hooks.kick_hook import kick_hook
from shinshi.extensions.moderation.utils.get_audit_reason import get_audit_reason
from shinshi.framework.interaction.context import Context
from shinshi.utils.emoji import get_emoji


class KickCommand(SlashCommand):
    def __init__(self, configuration_service: IConfigurationService) -> None:
        self.configuration_service: IConfigurationService = configuration_service
        super().__init__(
            name="kick",
            description=Localized(value="commands.kick.description"),
            default_member_permissions=Permissions.KICK_MEMBERS,
            options=[
                Option(
                    type=OptionType.USER,
                    name="member",
                    description=Localized(
                        value="commands.about.options.member.description"
                    ),
                ),
                Option(
                    type=OptionType.STRING,
                    name="reason",
                    description=Localized(
                        value="commands.about.options.reason.description"
                    ),
                    max_length=465,
                    is_required=False,
                ),
            ],
            hooks=[kick_hook],
        )

    async def send_member_notification(
        self, context: Context, member: Member, reason: str
    ) -> None:
        embed = (
            Embed(
                colour=Colour.YELLOW,
                timestamp=datetime.now(UTC),
            )
            .set_author(
                name=context.locale.get(
                    "commands.kick.target.embed.title", {"guild": context.guild.name}
                ),
                icon=context.guild.icon_url,
            )
            .add_field(
                name=context.locale.get("commands.kick.target.embed.fields.moderator"),
                value=f"@{context.member!s} (ID: {context.member.id})",
            )
            .add_field(
                name=context.locale.get("commands.kick.target.embed.fields.reason"),
                value=reason,
            )
        )
        try:
            await member.send(embed=embed)
        except BadRequestError as error:
            getLogger("shinshi.exceptions").warning(
                "failed to send notification to member in kick: %s", error
            )
        except Exception:  # pylint: disable=W0718
            pass

    async def callback(
        self, context: Context, member: Member, *, reason: str | None = None
    ) -> None:
        if reason is None:
            reason = context.locale.get("commands.kick.extra.no_reason")
        try:
            assert isinstance(context.guild, GatewayGuild)
            await context.guild.kick(
                member, reason=get_audit_reason(context.member, reason)
            )
        except ForbiddenError:
            return await context.create_error_response(
                context.locale.get("commands.kick.errors.forbidden_error")
            )
        except NotFoundError:
            return await context.create_error_response(
                context.locale.get("commands.kick.errors.not_found_error")
            )
        else:
            await context.create_response(
                context.locale.get(
                    "commands.kick.user.success",
                    {
                        "member": str(member),
                        "emoji": await context.bot.cache.get_application_emoji(
                            get_emoji(self.configuration_service, "success")
                        ),
                    },
                )
            )
            with contextlib.suppress():
                await self.send_member_notification(context, member, reason)
