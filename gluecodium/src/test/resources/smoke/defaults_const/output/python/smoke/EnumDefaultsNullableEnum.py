

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.Enum2 import Enum2


from _native_base import _NativeBase

import generated


class EnumDefaultsNullableEnum(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsNullableEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumDefaultsNullableEnum(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def enum_field1(self):
        return _wrap(self._native.enum_field1, Optional[Enum2])
    @enum_field1.setter
    def enum_field1(self, value):
      self._native.enum_field1 = _unwrap(value, Optional[Enum2])


    @property
    def enum_field1(self):
        return _wrap(self._native.enum_field1, Optional[Enum2])
    @enum_field1.setter
    def enum_field1(self, value):
      self._native.enum_field1 = _unwrap(value, Optional[Enum2])


