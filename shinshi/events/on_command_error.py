import contextlib
from logging import error

from aurum import events
from hikari.embeds import Embed

from shinshi.decorators.event import event
from shinshi.enums.colour import Colour


@event(events.CommandErrorEvent)
async def on_command_error(event: events.CommandErrorEvent) -> None:
    with contextlib.suppress(Exception):
        embed: Embed = Embed(
            colour=Colour.RED,
            description=event.context.locale.get(
                "events.command_error_event.embed.description"
            ),
        ).set_footer(
            event.context.locale.get("events.command_error_event.embed.footer")
        )

        await event.context.create_response(
            embed=embed,
            ephemeral=True,
        )

    error(
        "an unexpected error has occurred on %s in %s (guild: %s) with %s:",
        event.context.interaction.command_name,
        event.context.interaction.channel_id,
        event.context.interaction.guild_id,
        event.context.interaction.user.id,
        exc_info=event.exc_info,
    )
