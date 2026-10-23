

from enum import Enum
import typing
from typing import Optional

class ScalarKeyframe:
    def __init__(self, value: float, offset_in_ms: int) -> None: ...

    value: float

    offset_in_ms: int
