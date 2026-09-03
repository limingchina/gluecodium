

from smoke.FreeEnum import FreeEnum
from enum import Enum
import typing

class FreePoint:

    x: float

    y: float

    def flip(self) -> FreePoint:
        ...

    A_BAR = FreeEnum.BAR


