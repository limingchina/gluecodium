

from smoke.StructB import StructB
from enum import Enum
import typing
from typing import Optional

class StructA:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field: list[StructB]) -> None: ...

    field: list[StructB]
