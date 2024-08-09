import attrs
from aurum.context import InteractionContext

from shinshi.bot import Bot
from shinshi.client import Client
from shinshi.l10n.locale import Locale


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Context(InteractionContext):  # just for typing propouses
    bot: Bot
    client: Client

    locale: Locale
