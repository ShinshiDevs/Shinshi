from aurum.commands.slash_command import SlashCommand
from hikari.impl import MessageActionRowBuilder

from shinshi.extensions.general.consts import ORGANIZATION_URL, REPOSITORY_URL
from shinshi.framework.context.context import Context
from shinshi.framework.i18n.localized import Localized


class SourceCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(name="source", description=Localized("commands.source.description"))

    async def callback(self, context: Context) -> None:
        await context.create_response(
            components=[
                MessageActionRowBuilder()
                .add_link_button(REPOSITORY_URL, label=context.locale.get("commands.source.button.repository"))
                .add_link_button(ORGANIZATION_URL, label=context.locale.get("commands.source.button.organization"))
            ]
        )
