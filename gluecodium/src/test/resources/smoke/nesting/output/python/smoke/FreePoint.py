

from smoke.A_BAR import A_BAR
from smoke.FreePoint import FreePoint

class FreePoint:
    """"""

    def __init__(self, native):
        self._native = native


    x: float


    y: float


    def flip(self) -> FreePoint:
        """"""
        return self._native.flip()

