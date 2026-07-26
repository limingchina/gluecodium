

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from fire.Enum4 import Enum4
from smoke.EnumWrapper import EnumWrapper


from _native_base import _NativeBase

import generated


class EnumDefaultsWrappedEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_EnumDefaultsWrappedEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumDefaultsWrappedEnum(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> EnumWrapper:
        """"""
        return _wrap(self._native.struct_field, EnumWrapper)
    @struct_field.setter
    def struct_field(self, value: EnumWrapper):
      self._native.struct_field = _unwrap(value, EnumWrapper)


