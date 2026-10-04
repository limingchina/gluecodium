

from enum import Enum
import typing
from typing import Optional

class DartPublicElementsSkipped:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, bool_field: bool) -> None: ...

    bool_field: bool

    _string_field: str

    def _foo(self):
        ...
