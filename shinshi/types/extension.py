from importlib.machinery import ModuleSpec
from typing import TypedDict


class Extension(TypedDict):
    name: str
    commands: ModuleSpec
