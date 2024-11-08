import attrs
from aurum.commands.app_command import AppCommand


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Extension:
    name: str = attrs.field(repr=False, eq=False)
    package: str = attrs.field(repr=True, eq=True)
    commands: dict[str, AppCommand] = attrs.field(factory=dict, repr=False, eq=False)
