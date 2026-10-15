

from enum import Enum
import typing
from typing import Optional

class StructWithList:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: list[StructWithList]) -> None: ...

    field: list[StructWithList]
