

from __future__ import annotations

from fire.Enum4 import Enum4


from _native_base import _NativeBase

import generated


class EnumWrapper(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumWrapper):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumWrapper(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def enum_field(self) -> Enum4:
        """"""
        return Enum4(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: Enum4):
      self._native.enum_field = getattr(value, "_native", value)


