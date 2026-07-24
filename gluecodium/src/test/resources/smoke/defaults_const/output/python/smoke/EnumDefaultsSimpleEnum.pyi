

from fire.Enum1 import Enum1
import typing


from _native_base import _NativeBase

import generated


class EnumDefaultsSimpleEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsSimpleEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsSimpleEnum(*[_unwrap(arg) for arg in args]))


    @property
    def enum_field(self) -> Enum1:
        """"""
        return _wrap(self._native.enum_field, Enum1)
    @enum_field.setter
    def enum_field(self, value: Enum1):
      self._native.enum_field = _unwrap(value, Enum1)


