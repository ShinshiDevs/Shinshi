import attrs
from aurum.context import InteractionContext
from hikari.embeds import Embed

from shinshi.abc.i18n.ilocale import ILocale
from shinshi.enums.colour import Colour
from shinshi.framework.bot.bot import Bot


@attrs.define(eq=False, kw_only=True, hash=False, weakref_slot=False)
class Context(InteractionContext):
    bot: Bot = attrs.field(repr=False)
    locale: ILocale = attrs.field(repr=True)

    async def create_warning_response(
        self, title: str, *, description: str | None = None, ephemeral: bool = True
    ) -> None:
        return await self.create_response(
            embed=Embed(description=description, colour=Colour.YELLOW).set_author(name=title), ephemeral=ephemeral
        )

    async def create_error_response(
        self, title: str, *, description: str | None = None, ephemeral: bool = True
    ) -> None:
        return await self.create_response(
            embed=Embed(description=description, colour=Colour.RED).set_author(name=title), ephemeral=ephemeral
        )
