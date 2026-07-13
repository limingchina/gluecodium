

from smoke.A_BAR import A_BAR
from smoke.FreePoint import FreePoint

from _native_base import _NativeBase


class FreePoint(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    x: float


    y: float


    def flip(self) -> FreePoint:
        """"""
        return self._native.flip()

