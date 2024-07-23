from typing import Any
import attrs


@attrs.define(hash=False, weakref_slot=False, kw_only=True)
class Locale:
    name: str = attrs.field(eq=False, repr=True)
    value: dict[str, Any] = attrs.field(eq=True, repr=False)
