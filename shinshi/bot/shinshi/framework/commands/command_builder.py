from collections.abc import Callable

import hikari
from aurum.commands import impl
from aurum.commands.context_menu_command import ContextMenuCommand
from aurum.commands.options import Choice, Option
from aurum.commands.slash_command import SlashCommand, SlashCommandGroup
from aurum.commands.sub_command import SubCommand
from hikari.api import special_endpoints as api
from hikari.commands import CommandChoice, CommandOption, CommandType

from shinshi.abc.i18n.ii18n_provider import II18nProvider
from shinshi.framework.commands.locales import Locale
from shinshi.framework.i18n.localized import Localized


class CommandBuilder(impl.CommandBuilder):
    def __init__(self, i18n_provider: II18nProvider) -> None:
        self.i18n_provider: II18nProvider = i18n_provider

    def get_localizations(self, localized: Localized) -> dict[hikari.Locale | str, str]:
        return {
            Locale.to_hikari(name): locale.get(localized.key) for name, locale in self.i18n_provider.languages.items()
        }

    def localize(self, owner: object, attr_name: str) -> None:
        attr: Localized | str = getattr(owner, attr_name)
        if not isinstance(attr, Localized):
            return
        setattr(owner, attr_name, attr.resolve(self.i18n_provider.get_default_locale()))
        setattr(owner, f"{attr_name}_localizations", self.get_localizations(attr))

    def _build_slash_command(
        self, factory: Callable[[str, str], api.SlashCommandBuilder], command: SlashCommand
    ) -> api.SlashCommandBuilder:
        self.localize(command, "_name")
        self.localize(command, "_description")
        return super()._build_slash_command(factory, command)

    def _build_slash_command_group(
        self, factory: Callable[[str, str], api.SlashCommandBuilder], group: SlashCommandGroup
    ) -> api.SlashCommandBuilder:
        self.localize(group, "_name")
        return super()._build_slash_command_group(factory, group)

    def _build_sub_command(self, command: SubCommand) -> CommandOption:
        self.localize(command, "name")
        self.localize(command, "description")
        return super()._build_sub_command(command)

    def _build_choice(self, choice: Choice) -> CommandChoice:
        self.localize(choice, "name")
        return super()._build_choice(choice)

    def _build_option(self, option: Option) -> CommandOption:
        self.localize(option, "name")
        self.localize(option, "description")
        return super()._build_option(option)

    def _build_context_menu_command(
        self, factory: Callable[[CommandType, str], api.ContextMenuCommandBuilder], command: ContextMenuCommand
    ) -> api.ContextMenuCommandBuilder:
        self.localize(command, "_name")
        self.localize(command, "_description")
        return super()._build_context_menu_command(factory, command)
