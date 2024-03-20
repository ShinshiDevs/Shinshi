from typing import Dict

from hikari import impl

from shinshi.discord.interactables.slash_command import SlashCommand
from shinshi.discord.models.translatable import Translatable
from shinshi.discord.workflows.builders.utils import convert_option
from shinshi.i18n import I18nProvider


class SlashCommandBuilder:
    def __init__(
        self,
        command: SlashCommand,
        i18n_provider: I18nProvider,
    ) -> None:
        self.command: SlashCommand = command
        self.i18n_provider: I18nProvider = i18n_provider

    def build(self) -> (SlashCommand, impl.SlashCommandBuilder):
        descriptions: Dict[str, str] | None = None
        if isinstance(self.command.description, Translatable):
            descriptions = self.command.description.translate(self.i18n_provider)
        builder: impl.SlashCommandBuilder = impl.SlashCommandBuilder(
            name=self.command.name or self.command.callback.__name__,
            description=getattr(self.command.description, "fallback", self.command.description),
            description_localizations=descriptions,
            options=list(
                convert_option(option, self.i18n_provider) for option in
                self.command.options or ()
            ),
            default_member_permissions=self.command.default_member_permissions,
            is_dm_enabled=self.command.is_dm_enabled,
            is_nsfw=self.command.is_nsfw,
        )
        return self.command, builder
