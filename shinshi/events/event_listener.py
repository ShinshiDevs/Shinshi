from typing import Coroutine, Callable, Any, TypeVar, Type

from shinshi.events.base_event import BaseEvent

InstanceT = TypeVar("InstanceT")
EventListenerCallback = TypeVar(
    "EventListenerCallback", bound=Callable[[Any], Coroutine[Any, Any, None]]
)


class EventListener:
    def __init__(
        self,
        event: Type[BaseEvent],
        callback: EventListenerCallback,
        instance: InstanceT = None,
    ) -> None:
        self.event = event
        self.callback = callback
        self.__instance = instance

    @property
    def instance(self) -> InstanceT:
        return self.__instance

    @instance.setter
    def instance(self, instance: InstanceT) -> None:
        self.__instance = instance

    def __call__(self, *args, **kwargs) -> EventListenerCallback:
        return self.callback(self.instance, *args, **kwargs)
