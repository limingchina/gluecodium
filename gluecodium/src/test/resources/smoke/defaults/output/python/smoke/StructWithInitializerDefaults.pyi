

from enum import Enum
import typing
from typing import Optional

class StructWithInitializerDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, ints_field: list[int], floats_field: list[float], set_type_field: set[str], map_field: dict[int, str]) -> None: ...

    ints_field: list[int]

    floats_field: list[float]

    set_type_field: set[str]

    map_field: dict[int, str]
