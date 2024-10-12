from aurum.context import InteractionContext

from shinshi.bot import Bot
from shinshi.i18n.types import Locale


class Context(InteractionContext):
    bot: Bot
    locale: Locale
