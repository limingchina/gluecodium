

from __future__ import annotations

from fire.ExternalEnum2 import ExternalEnum2


from _native_base import _NativeBase

import generated


class EnumDefaultsExternalNullableEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsExternalNullableEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsExternalNullableEnum(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def enum_field1(self):
        """"""
        return Optional[ExternalEnum2](self._native.enum_field1)
    @enum_field1.setter
    def enum_field1(self, value):
      self._native.enum_field1 = getattr(value, "_native", value)



    @property
    def enum_field2(self):
        """"""
        return Optional[ExternalEnum2](self._native.enum_field2)
    @enum_field2.setter
    def enum_field2(self, value):
      self._native.enum_field2 = getattr(value, "_native", value)


