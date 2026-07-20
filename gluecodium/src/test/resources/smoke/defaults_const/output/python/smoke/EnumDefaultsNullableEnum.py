

from __future__ import annotations

from fire.Enum2 import Enum2


from _native_base import _NativeBase

import generated


class EnumDefaultsNullableEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsNullableEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsNullableEnum(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def enum_field1(self):
        """"""
        return Optional[Enum2](self._native.enum_field1)
    @enum_field1.setter
    def enum_field1(self, value):
      self._native.enum_field1 = getattr(value, "_native", value)



    @property
    def enum_field1(self):
        """"""
        return Optional[Enum2](self._native.enum_field1)
    @enum_field1.setter
    def enum_field1(self, value):
      self._native.enum_field1 = getattr(value, "_native", value)


