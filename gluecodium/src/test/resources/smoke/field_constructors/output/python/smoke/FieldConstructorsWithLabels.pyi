

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsWithLabels:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int, bool_field: bool) -> None: ...
    @typing.overload
    def __init__(self, string_field: str, int_field: int, bool_field: bool) -> None: ...

    string_field: str

    int_field: int

    bool_field: bool
