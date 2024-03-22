from typing import Any, ClassVar, Dict, Literal, Self, Type, TypeVar, overload

from shinshi.di.exceptions import InjectionError

T = TypeVar("T")
InstanceT = TypeVar("InstanceT")


class DependencyInjection:
    container: ClassVar[Dict[str | Type, Any]] = dict()
    key: str | Type[T]

    def __init__(self, key: str | type[T]) -> None:
        self.key = key

    @property
    def value(self) -> T:
        return self.get(self.key)

    @overload
    def __get__(self, instance: InstanceT, cls: Type[InstanceT] | None = None) -> T:
        ...

    @overload
    def __get__(self, instance: Literal[None], cls: Type[InstanceT]) -> "Self":
        ...

    def __get__(
        self,
        instance: InstanceT | None,
        cls: type[InstanceT] | None = None
    ) -> T | "Self":
        if instance is None:
            return self
        return self.value

    @classmethod
    def store(cls, value: T, key: str | Type[T] | None = None) -> T:
        if key is None:
            key = type(value)
        cls.container[key] = value

    @classmethod
    def get(cls, key: str | Type[T]) -> T:
        value = cls.container.get(key)
        if value is None:
            raise InjectionError(key)
        return value
