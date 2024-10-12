from shinshi.types.events import EventCallback, EventType


def event(event_type: EventType) -> EventCallback:
    def inner(func: EventCallback) -> EventCallback:
        setattr(func, "__event_type", event_type)
        return func

    return inner
