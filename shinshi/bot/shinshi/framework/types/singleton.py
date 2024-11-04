from typing import Type, TypeVar

T = TypeVar("T", bound="Singleton")


class Singleton:
    _instance: T | None = None

    def __new__(cls: Type[T], *args, **kwargs) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
