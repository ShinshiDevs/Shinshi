from collections.abc import Sequence

from shinshi.extensions.general.commands.about_command import AboutCommand
from shinshi.extensions.general.commands.stats_command import StatsCommand

__all__: Sequence[str] = ("StatsCommand", "AboutCommand")
