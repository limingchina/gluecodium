

import typing


from _native_base import _NativeBase

import generated


class VeryBoolean(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.VeryBoolean):
            super().__init__(args[0])
        else:
            super().__init__(generated.VeryBoolean(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def value(self) -> bool:
        """"""
        return self._native.value
    @value.setter
    def value(self, value: bool):
      self._native.value = getattr(value, "_native", value)


    @staticmethod
    def make(value: bool) -> VeryBoolean: ...

