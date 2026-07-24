

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from fire.Enum3 import Enum3


from _native_base import _NativeBase

import generated


class EnumDefaultsAliasEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsAliasEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsAliasEnum(*[_unwrap(arg) for arg in args]))


    @property
    def enum_field(self) -> Enum3:
        """"""
        return _wrap(self._native.enum_field, Enum3)
    @enum_field.setter
    def enum_field(self, value: Enum3):
      self._native.enum_field = _unwrap(value, Enum3)


