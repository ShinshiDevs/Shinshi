from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class I18nGroup:
    name: str
    value: Dict[str, str | I18nGroup | Tuple[str, ...]] = field(default_factory=dict)
