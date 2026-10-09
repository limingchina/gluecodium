

from enum import Enum
import typing
from typing import Optional

class SomeDartStructWithTypedefField:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, some_field: list[float]) -> None: ...

    some_field: list[float]
