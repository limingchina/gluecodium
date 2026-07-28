

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.ExternalEnum3 import ExternalEnum3


from _native_base import _NativeBase

import generated


class EnumDefaultsExternalAliasEnum(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumDefaultsExternalAliasEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumDefaultsExternalAliasEnum(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def enum_field(self) -> ExternalEnum3:
        """"""
        return _wrap(self._native.enum_field, ExternalEnum3)
    @enum_field.setter
    def enum_field(self, value: ExternalEnum3):
      self._native.enum_field = _unwrap(value, ExternalEnum3)


