from collections.abc import Sequence
from typing import ValuesView

from aurum.commands import SlashCommand
from aurum.commands.decorators import sub_command
from aurum.l10n import Localized
from hikari.channels import ChannelType, GuildChannel
from hikari.embeds import Embed
from hikari.guilds import GatewayGuild
from hikari.impl import LinkButtonBuilder, MessageActionRowBuilder

from shinshi.ext.colour import Colour
from shinshi.sdk.context import Context
from shinshi.utils.datetime import format_datetime


def get_channel_amount(
    channels: Sequence[GuildChannel], channel_type: ChannelType
) -> int:
    return sum(channel.type == channel_type for channel in channels)


class GuildCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("guild")

    @sub_command(
        "info",
        description=Localized(value="commands.user.info.description"),
    )
    async def user_info(
        self,
        context: Context,
    ) -> None:
        guild: GatewayGuild = context.guild
        channels: ValuesView[GuildChannel] = guild.get_channels().values()
        embed: Embed = (
            Embed(description=guild.description, colour=Colour.GREY)
            .set_author(name=guild.name)
            .set_thumbnail(guild.icon_url)
            .set_footer(
                context.locale.get(
                    "commands.guild.info.footer",
                    {"guild_id": guild.id, "shard_id": guild.shard_id},
                )
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.ownership"),
                value=f"<@!{guild.owner_id}>",
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.created_at"),
                value=format_datetime(guild.created_at, "D"),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.members"),
                value=guild.member_count,
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.categories"),
                value=get_channel_amount(channels, ChannelType.GUILD_CATEGORY),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.text"),
                value=get_channel_amount(channels, ChannelType.GUILD_TEXT),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.voice"),
                value=get_channel_amount(channels, ChannelType.GUILD_VOICE),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.roles"),
                value=len(guild.get_roles()),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.emojis"),
                value=len(guild.get_emojis()),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.stickers"),
                value=len(guild.get_stickers()),
                inline=True,
            )
            .add_field(
                name=context.locale.get("commands.guild.info.fields.boost.name"),
                value=context.locale.get(
                    "commands.guild.info.fields.boost.boosted",
                    {
                        "level": guild.premium_tier,
                        "subscribers": guild.premium_subscription_count,
                    },
                )
                if guild.premium_subscription_count
                else context.locale.get("commands.guild.info.fields.boost.none"),
                inline=True,
            )
            .add_field(
                name=context.locale.get(
                    "commands.guild.info.fields.verification_level.name"
                ),
                value=context.locale.get(
                    "commands.guild.info.fields.verification_level.level"
                )[guild.verification_level.value],
                inline=True,
            )
        )

        components: Sequence[LinkButtonBuilder] = []
        if guild.splash_url:
            components.append(
                LinkButtonBuilder(
                    label=context.locale.get("commands.guild.info.buttons.splash"),
                    url=guild.splash_url,
                )
            )
        if guild.banner_url:
            components.append(
                LinkButtonBuilder(
                    label=context.locale.get("commands.guild.info.buttons.banner"),
                    url=guild.banner_url,
                )
            )

        return await context.create_response(
            embed=embed,
            component=(
                MessageActionRowBuilder(components=components) if components else None
            ),
        )
