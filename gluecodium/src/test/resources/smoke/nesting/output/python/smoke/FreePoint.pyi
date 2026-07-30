

from smoke.FreeEnum import FreeEnum
import typing

class FreePoint:

    x: float

    y: float

    def flip(self) -> FreePoint:
        ...

    A_BAR = FreeEnum.BAR

