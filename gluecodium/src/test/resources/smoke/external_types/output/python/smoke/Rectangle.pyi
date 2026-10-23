

from enum import Enum
import typing
from typing import Optional

class Rectangle:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, left: int, top: int, width: int, height: int) -> None: ...

    left: int

    top: int

    width: int

    height: int
