from aurum.context import InteractionContext
from hikari.embeds import Embed

from shinshi.enums.colour import Colour
from shinshi.framework.bot.bot import Bot
from shinshi.framework.i18n.locale import Locale


class Context(InteractionContext):
    bot: Bot
    locale: Locale

    async def create_warning_response(self, title: str, *, description: str | None = None) -> None:
        return await self.create_response(
            embed=(Embed(description=description, colour=Colour.GREY).set_author(name=title)), ephemeral=True
        )

    async def create_error_response(self, title: str, *, description: str | None = None) -> None:
        return await self.create_response(
            embed=(Embed(description=description, colour=Colour.GREY).set_author(name=title)), ephemeral=True
        )
