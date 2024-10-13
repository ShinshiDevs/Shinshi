from collections.abc import Callable
from typing import Any, TypeVar

from hikari import events

EventT = TypeVar("EventT", bound=events.Event)
EventCallback = Callable[[EventT], Any]
