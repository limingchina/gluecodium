

from enum import Enum
import typing
from typing import Optional

class SomeStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, int_field: int) -> None: ...

    int_field: int
