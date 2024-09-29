from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, ClassVar, TypeVar

from hikari import events

EventType = TypeVar("EventType", bound=events.Event)


class EventMeta(ABCMeta):
    def __new__(
        cls, name: str, bases: tuple[type], dict: dict[str, Any], **kwargs: Any
    ) -> EventMeta:
        cls: EventMeta = super().__new__(cls, name, bases, dict)
        if event_type := kwargs.get("type"):
            cls.__event_type__ = event_type
        return cls


class Event(ABC, metaclass=EventMeta):
    __event_type__: ClassVar[EventType]

    @classmethod
    def event_type(cls) -> EventType:
        return cls.__event_type__

    @abstractmethod
    async def callback(self, event: EventType) -> Any: ...
