

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class FreePoint(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.FreePoint):
            super().__init__(args[0])
        else:
            super().__init__(generated.FreePoint(*[_unwrap(arg) for arg in args]))


    @property
    def x(self) -> float:
        """"""
        return _wrap(self._native.x, float)
    @x.setter
    def x(self, value: float):
      self._native.x = _unwrap(value, float)



    @property
    def y(self) -> float:
        """"""
        return _wrap(self._native.y, float)
    @y.setter
    def y(self, value: float):
      self._native.y = _unwrap(value, float)


    def flip(self) -> FreePoint:
        """"""
        return _wrap(self._native.flip(), FreePoint)


    A_BAR = FreeEnum.BAR

