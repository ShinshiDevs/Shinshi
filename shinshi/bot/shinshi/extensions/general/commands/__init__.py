from collections.abc import Sequence

from shinshi.extensions.general.commands.about_command import AboutCommand
from shinshi.extensions.general.commands.source_command import SourceCommand
from shinshi.extensions.general.commands.stats_command import StatsCommand
from shinshi.extensions.general.commands.support_command import SupportCommand

__all__: Sequence[str] = ("StatsCommand", "AboutCommand", "SourceCommand", "SupportCommand")
