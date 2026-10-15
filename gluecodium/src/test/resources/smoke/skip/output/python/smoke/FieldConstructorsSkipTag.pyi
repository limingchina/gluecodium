

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsSkipTag:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field1: str) -> None: ...

    field1: str
