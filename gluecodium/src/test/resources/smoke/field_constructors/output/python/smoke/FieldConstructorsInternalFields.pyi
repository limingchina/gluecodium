

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsInternalFields:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int, string_field: str) -> None: ...

    string_field: str

    int_field: int

    _bool_field: bool
