

from smoke.SomeSkippedEnum import SomeSkippedEnum
from enum import Enum
import typing
from typing import Optional

class SomeSkippedStruct:
    def __eq__(self, other: object) -> bool: ...
    __hash__ = None  # type: ignore[assignment]
    def as_key(self) -> _gluecodium_key_736d6f6b652e536f6d65536b6970706564537472756374: ...

    field: list[SomeSkippedEnum]



class _gluecodium_key_736d6f6b652e536f6d65536b6970706564537472756374(SomeSkippedStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
