from shinshi.types.events import EventCallback, EventT


def event(event_type: EventT) -> EventCallback:
    def inner(func: EventCallback) -> EventCallback:
        setattr(func, "__event_type", event_type)
        return func

    return inner
