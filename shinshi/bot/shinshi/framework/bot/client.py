from aurum.client import Client as _Client
from hikari.interactions import (
    BaseCommandInteraction,
    ComponentInteraction,
)

from shinshi.framework.interaction.context import Context


class Client(_Client):
    def create_context(
        self, interaction: BaseCommandInteraction | ComponentInteraction
    ) -> Context:
        return Context(
            interaction=interaction,
            bot=self.bot,
            client=self,
            locale=self.l10n.get_locale(interaction) if self.l10n else None,
        )
