

from enum import Enum
import typing
from typing import Optional

class StructWithAllDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int, string_field: str) -> None: ...

    int_field: int

    string_field: str
