

from enum import Enum
import typing
from typing import Optional

class SomeMutableCustomStructWithDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int, string_field: str, list_field: list[int]) -> None: ...

    int_field: int

    string_field: str

    list_field: list[int]
