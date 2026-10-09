

from enum import Enum
import typing
from typing import Optional

class DartInternalElementsEnabled:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, bool_field: bool, string_field: str) -> None: ...

    bool_field: bool

    string_field: str

    def foo(self):
        ...
