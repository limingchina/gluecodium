

from smoke.StructA import StructA
from enum import Enum
import typing
from typing import Optional

class StructB:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: list[StructA]) -> None: ...

    field: list[StructA]
