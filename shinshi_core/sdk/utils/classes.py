def get_full_name(__class: type) -> str:
    module_name, class_name = __class.__module__, __class.__qualname__
    if module_name in (None, str.__class__.__module__):
        return class_name
    return ".".join((module_name, class_name))
