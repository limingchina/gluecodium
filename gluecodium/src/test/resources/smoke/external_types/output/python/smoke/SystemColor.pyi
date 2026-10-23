

from enum import Enum
import typing
from typing import Optional

class SystemColor:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, red: float, green: float, blue: float, alpha: float) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    __hash__ = None  # type: ignore[assignment]
    def as_key(self) -> _gluecodium_key_736d6f6b652e53797374656d436f6c6f72: ...

    red: float

    green: float

    blue: float

    alpha: float



class _gluecodium_key_736d6f6b652e53797374656d436f6c6f72(SystemColor):
    def __hash__(self) -> int: ...  # type: ignore[override]
