from aurum.commands.slash_command import SlashCommand
from hikari.impl import MessageActionRowBuilder

from shinshi.extensions.general.consts import SUPPORT_URL
from shinshi.framework.context.context import Context
from shinshi.framework.i18n.localized import Localized


class SupportCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(name="support", description=Localized("commands.support.description"))

    async def callback(self, context: Context) -> None:
        await context.create_response(
            components=[
                MessageActionRowBuilder().add_link_button(
                    SUPPORT_URL, label=context.locale.get("commands.support.button.discord")
                )
            ]
        )
