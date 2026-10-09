

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsCppSkip:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, string_field: str, int_field: int) -> None: ...

    string_field: str

    int_field: int
