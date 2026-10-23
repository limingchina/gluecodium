

from enum import Enum
import typing
from typing import Optional

class StructWithMap:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: dict[str, StructWithMap]) -> None: ...

    field: dict[str, StructWithMap]
