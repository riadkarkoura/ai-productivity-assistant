from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AssistantTask:
    number: str
    title: str
    handler: Callable[[], None]
