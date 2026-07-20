

from __future__ import annotations

from fire.Enum1 import Enum1


from _native_base import _NativeBase

import generated


class EnumDefaultsSimpleEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsSimpleEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsSimpleEnum(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def enum_field(self) -> Enum1:
        """"""
        return Enum1(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: Enum1):
      self._native.enum_field = getattr(value, "_native", value)


