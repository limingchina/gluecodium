

from enum import Enum
import typing

class StructWithSet:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    field: set[StructWithSet]


