

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.Enum1 import Enum1


from _native_base import _NativeBase

import generated


class EnumDefaultsSimpleEnum(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsSimpleEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumDefaultsSimpleEnum(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def enum_field(self) -> Enum1:
        """"""
        return _wrap(self._native.enum_field, Enum1)
    @enum_field.setter
    def enum_field(self, value: Enum1):
      self._native.enum_field = _unwrap(value, Enum1)


