

from enum import Enum
import typing
from typing import Optional

class StructWithSet:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: set[StructWithSet]) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    __hash__ = None  # type: ignore[assignment]
    def as_key(self) -> _gluecodium_key_736d6f6b652e53747275637457697468536574: ...

    field: set[StructWithSet]



class _gluecodium_key_736d6f6b652e53747275637457697468536574(StructWithSet):
    def __hash__(self) -> int: ...  # type: ignore[override]
