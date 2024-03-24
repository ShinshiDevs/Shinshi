from orjson import dumps


def orjson_serialize(data: bytes) -> str:
    return dumps(data).decode("UTF-8")
