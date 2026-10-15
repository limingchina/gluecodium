

from enum import Enum
import typing
from typing import Optional

class SkipFieldInPlatformImmutable:
    def __init__(self, int_field: int, bool_field: bool) -> None: ...

    int_field: int

    bool_field: bool
