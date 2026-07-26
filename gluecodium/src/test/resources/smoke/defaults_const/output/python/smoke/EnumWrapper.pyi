

from fire.Enum4 import Enum4
import typing


from _native_base import _NativeBase

import generated


class EnumWrapper(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_EnumWrapper):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumWrapper(*[_unwrap(arg) for arg in args]))


    @property
    def enum_field(self) -> Enum4:
        """"""
        return _wrap(self._native.enum_field, Enum4)
    @enum_field.setter
    def enum_field(self, value: Enum4):
      self._native.enum_field = _unwrap(value, Enum4)


