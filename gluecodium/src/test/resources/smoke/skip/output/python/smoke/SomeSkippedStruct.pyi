

from smoke.SomeSkippedEnum import SomeSkippedEnum
from enum import Enum
import typing

class SomeSkippedStruct:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    field: list[SomeSkippedEnum]


