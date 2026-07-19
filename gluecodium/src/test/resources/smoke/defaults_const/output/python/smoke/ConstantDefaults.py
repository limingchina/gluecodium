

from __future__ import annotations

from fire.SomeStruct import SomeStruct


from _native_base import _NativeBase

import generated


class ConstantDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ConstantDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.ConstantDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field1(self) -> SomeStruct:
        """"""
        return SomeStruct(self._native.field1)
    @field1.setter
    def field1(self, value: SomeStruct):
      self._native.field1 = getattr(value, "_native", value)



    @property
    def field2(self) -> SomeStruct:
        """"""
        return SomeStruct(self._native.field2)
    @field2.setter
    def field2(self, value: SomeStruct):
      self._native.field2 = getattr(value, "_native", value)


