from aurum.context import InteractionContext

from shinshi.framework.bot.bot import Bot
from shinshi.framework.i18n.locale import Locale


class Context(InteractionContext):
    bot: Bot
    locale: Locale
