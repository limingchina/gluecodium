

from enum import Enum
import typing
from typing import Optional

class DummyStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, string_field: str) -> None: ...

    string_field: str
