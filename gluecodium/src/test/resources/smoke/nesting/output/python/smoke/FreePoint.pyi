

from smoke.FreeEnum import FreeEnum
from enum import Enum
import typing
from typing import Optional

class FreePoint:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float) -> None: ...

    x: float

    y: float

    def flip(self) -> FreePoint:
        ...


    A_BAR = FreeEnum.BAR
