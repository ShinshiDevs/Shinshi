# Thanks to LightmanLP for this solution (only suggestion).=
from asyncio import iscoroutinefunction
from typing import Dict, List, Type

from shinshi.events.base_event import BaseEvent
from shinshi.events.event_listener import EventListener, EventListenerCallback


class EventManager:
    def __init__(self):
        self.listeners: Dict[Type[BaseEvent], List[EventListener]] = {}

    def subscribe(self, event: Type[BaseEvent], listener: EventListener) -> None:
        if not iscoroutinefunction(listener.callback):
            raise ValueError("Callback of event listener must me a asynchronous")
        self.listeners.setdefault(event, []).append(listener)

    async def emit(self, event: Type[BaseEvent], *args, **kwargs):
        for listener in self.listeners.get(event, []):
            await listener(*args, **kwargs)


event_manager: EventManager = EventManager()


def subscribe_event(event_type: Type[BaseEvent]):
    def decorator(func: EventListenerCallback) -> EventListener:
        return EventListener(event_type, func)

    return decorator
