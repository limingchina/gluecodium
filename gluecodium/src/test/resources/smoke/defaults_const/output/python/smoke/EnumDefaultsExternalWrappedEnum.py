

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.ExternalEnum4 import ExternalEnum4
from smoke.EnumWrapper import EnumWrapper


from _native_base import _NativeBase

import generated


class EnumDefaultsExternalWrappedEnum(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsExternalWrappedEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumDefaultsExternalWrappedEnum(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def struct_field(self) -> EnumWrapper:
        return _wrap(self._native.struct_field, EnumWrapper)
    @struct_field.setter
    def struct_field(self, value: EnumWrapper):
      self._native.struct_field = _unwrap(value, EnumWrapper)


