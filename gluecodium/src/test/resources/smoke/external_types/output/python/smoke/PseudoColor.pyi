

from enum import Enum
import typing
from typing import Optional

class PseudoColor:
    def __eq__(self, other: object) -> bool: ...
    __hash__ = None  # type: ignore[assignment]
    def as_key(self) -> _gluecodium_key_736d6f6b652e50736575646f436f6c6f72: ...

    red: float

    green: float

    blue: float

    alpha: float



class _gluecodium_key_736d6f6b652e50736575646f436f6c6f72(PseudoColor):
    def __hash__(self) -> int: ...  # type: ignore[override]
