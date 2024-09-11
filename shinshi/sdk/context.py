import attrs
from aurum.context import InteractionContext

from shinshi.sdk.bot import Bot
from shinshi.sdk.client import Client
from shinshi.i18n.locale import Locale


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Context(InteractionContext):
    bot: Bot
    client: Client

    locale: Locale
