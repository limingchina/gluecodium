

import typing


from _native_base import _NativeBase

import generated


class MethodOverloadsPoint(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.MethodOverloadsPoint):
            super().__init__(args[0])
        else:
            super().__init__(generated.MethodOverloadsPoint(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def x(self) -> float:
        """"""
        return self._native.x
    @x.setter
    def x(self, value: float):
      self._native.x = getattr(value, "_native", value)



    @property
    def y(self) -> float:
        """"""
        return self._native.y
    @y.setter
    def y(self, value: float):
      self._native.y = getattr(value, "_native", value)


