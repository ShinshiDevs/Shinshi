from collections.abc import Callable
from typing import Any, TypeVar

from hikari import events

EventType = TypeVar("EventType", bound=events.Event)
EventCallback = Callable[[EventType], Any]
