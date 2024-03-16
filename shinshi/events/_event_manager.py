# Thanks to LightmanLP for this solution (only suggestion).
import asyncio
from typing import Coroutine, Dict, List, Callable, Type, Any

from shinshi.events.base_event import BaseEvent


class EventManager:
    def __init__(self):
        self.listeners: Dict[Type[BaseEvent], List[Callable[[], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, event: Type[BaseEvent], callback: Callable[[], Coroutine[Any, Any, None]]) -> None:
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback must be an asynchronous function")
        if not isinstance(event(), BaseEvent):
            raise TypeError("Event must inherit from BaseEvent")
        self.listeners.setdefault(event, []).append(callback)

    async def send(self, event: Type[BaseEvent]) -> None:
        handlers: List[Callable[[], Coroutine[Any, Any, None]]] = self.listeners.get(event, [])
        await asyncio.gather(*(handler() for handler in handlers))


event_manager: EventManager = EventManager()
