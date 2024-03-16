from shinshi.events._event_manager import event_manager
from shinshi.events.event_listener import EventListener


class RegisterEventsMeta(type):
    def __new__(cls, name, bases, namespace):
        new_cls = super(RegisterEventsMeta, cls).__new__(cls, name, bases, namespace)
        new_cls._event_methods = {
            attr_name: attr_value
            for attr_name, attr_value in namespace.items()
            if isinstance(attr_value, EventListener)
        }
        return new_cls

    def __call__(cls, *args, **kwargs):
        instance = super(RegisterEventsMeta, cls).__call__(*args, **kwargs)
        for _, listener in cls._event_methods.items():
            listener.instance = instance
            event_manager.subscribe(listener.event, listener)
        return instance
