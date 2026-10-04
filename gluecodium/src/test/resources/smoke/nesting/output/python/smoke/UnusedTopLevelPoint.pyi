

from enum import Enum
import typing
from typing import Optional

class UnusedTopLevelPoint:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, foo: str) -> None: ...

    foo: str
