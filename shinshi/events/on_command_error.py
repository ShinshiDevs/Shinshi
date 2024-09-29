from traceback import format_exception

from aurum import events
from hikari.embeds import Embed

from shinshi.ext.colour import Colour
from shinshi.sdk.context import Context
from shinshi.sdk.event import Event
from shinshi.utils.codeblock import get_codeblock


class CommandErrorEvent(Event, type=events.CommandErrorEvent):
    @staticmethod
    async def callback(event: events.CommandErrorEvent) -> None:
        context: Context = event.context

        embed: Embed = Embed(
            colour=Colour.RED,
            description=context.locale.get(
                "events.command_error_event.embed.description"
            ),
        ).set_footer(context.locale.get("events.command_error_event.embed.footer"))

        if (await context.bot.cache.get_application()).team.members.get(
            context.user.id
        ):
            exc_type, exc_value, exc_traceback = event.exc_info
            embed.add_field(
                name=context.locale.get(
                    "events.command_error_event.embed.fields.details"
                ),
                value=get_codeblock(
                    "py", "".join(format_exception(exc_type, exc_value, exc_traceback))
                ),
                inline=False,
            )

        await context.create_response(
            embed=embed,
            ephemeral=True,
        )
