



from _native_base import _NativeBase

import generated


class FreePoint(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], FreePoint):
            super().__init__(args[0])
        else:
            super().__init__(generated.FreePoint(*args))


    @property
    def x(self) -> float:
        """"""
        return self._native.x

    @x.setter
    def x(self, value: float):
        self._native.x = value



    @property
    def y(self) -> float:
        """"""
        return self._native.y

    @y.setter
    def y(self, value: float):
        self._native.y = value



    def flip(self) -> FreePoint:
        """"""
        return self._native.flip()


A_BAR = FreeEnum.BAR

