from dataclasses import dataclass


@dataclass
class HookResult:
    exit: bool = False
