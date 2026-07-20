

import typing


from _native_base import _NativeBase

import generated


class TypeDefsTestStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeDefsTestStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeDefsTestStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def something(self) -> str:
        """"""
        return self._native.something
    @something.setter
    def something(self, value: str):
      self._native.something = getattr(value, "_native", value)


