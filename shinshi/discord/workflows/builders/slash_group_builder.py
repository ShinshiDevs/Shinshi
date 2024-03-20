from typing import List, Sequence, Dict

from hikari import impl, OptionType, CommandOption

from shinshi.discord.interactables.group import Group
from shinshi.discord.interactables.slash_command import SlashCommand
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.builders.utils import convert_option
from shinshi.i18n import I18nProvider


class SlashGroupBuilder:
    def __init__(
        self,
        group: Group,
        commands: List[SlashCommand],
        i18n_provider: I18nProvider,
    ) -> None:
        self.group: Group = group
        self.commands: List[SlashCommand] = commands
        self.i18n_provider: I18nProvider = i18n_provider

    def build(self) -> (Sequence[SlashCommand], impl.SlashCommandBuilder):
        builder: impl.SlashCommandBuilder = impl.SlashCommandBuilder(
            name=self.group.name,
            description="-",
            default_member_permissions=self.group.default_member_permissions,
            is_dm_enabled=self.group.is_dm_enabled,
            is_nsfw=self.group.is_nsfw,
        )
        for command in self.commands:
            descriptions: Dict[str, str] | None = None
            if isinstance(command.description, Translatable):
                descriptions = command.description.translate(self.i18n_provider)
            builder.add_option(
                CommandOption(
                    type=OptionType.SUB_COMMAND,
                    name=command.name,
                    description=getattr(command.description, "fallback", command.description),
                    description_localizations=descriptions,
                    options=list(
                        convert_option(option, self.i18n_provider) for option in command.options
                    )
                )
            )
        return self.commands, builder
