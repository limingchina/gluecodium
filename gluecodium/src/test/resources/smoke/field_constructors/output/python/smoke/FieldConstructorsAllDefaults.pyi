

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsAllDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int) -> None: ...
    @typing.overload
    def __init__(self, int_field: int, string_field: str) -> None: ...
    @typing.overload
    def __init__(self, bool_field: bool, int_field: int, string_field: str) -> None: ...

    string_field: str

    int_field: int

    bool_field: bool
