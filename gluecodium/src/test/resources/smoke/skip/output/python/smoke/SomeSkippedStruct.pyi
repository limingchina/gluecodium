

from smoke.SomeSkippedEnum import SomeSkippedEnum
import typing

class SomeSkippedStruct:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    field: list[SomeSkippedEnum]

