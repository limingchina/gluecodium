

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.FooBarEnum import FooBarEnum


from _native_base import _NativeBase

import generated


class InternalEnumDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_InternalEnumDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_InternalEnumDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def public_field(self) -> FooBarEnum:
        """"""
        return _wrap(self._native.public_field, FooBarEnum)
    @public_field.setter
    def public_field(self, value: FooBarEnum):
      self._native.public_field = _unwrap(value, FooBarEnum)



    @property
    def public_list_field(self) -> list[FooBarEnum]:
        """"""
        return _wrap(self._native.public_list_field, list[FooBarEnum])
    @public_list_field.setter
    def public_list_field(self, value: list[FooBarEnum]):
      self._native.public_list_field = _unwrap(value, list[FooBarEnum])


