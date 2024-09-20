import time

from aurum.commands import SlashCommand
from aurum.l10n import Localized

from shinshi.sdk.context import Context


class PingCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(
            "ping", description=Localized(value="commands.ping.description")
        )

    async def callback(self, context: Context) -> None:
        time_start: float = time.perf_counter()
        await context.defer(ephemeral=True)
        rest_latency: float = time.perf_counter() - time_start

        return await context.edit_response(
            context.locale.get(
                "commands.ping.message",
                {
                    "bot_latency": f"{context.bot.heartbeat_latency * 1_000:.1f}",
                    "rest_latency": f"{rest_latency  * 1_000:.1f}",
                },
            )
        )
