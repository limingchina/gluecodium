

from enum import Enum
import typing
from typing import Optional

class StructWithConstMethod:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, string_field: str) -> None: ...

    string_field: str

    def double_const(self) -> float:
        ...
