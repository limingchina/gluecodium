

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.FooBarEnum import FooBarEnum


from _native_base import _NativeBase

import generated


class InternalEnumDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.InternalEnumDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.InternalEnumDefaults(*[_unwrap(arg) for arg in args]))


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



    @property
    def internal_field(self) -> FooBarEnum:
        """"""
        return _wrap(self._native.internal_field, FooBarEnum)
    @internal_field.setter
    def internal_field(self, value: FooBarEnum):
      self._native.internal_field = _unwrap(value, FooBarEnum)



    @property
    def internal_list_field(self) -> list[FooBarEnum]:
        """"""
        return _wrap(self._native.internal_list_field, list[FooBarEnum])
    @internal_list_field.setter
    def internal_list_field(self, value: list[FooBarEnum]):
      self._native.internal_list_field = _unwrap(value, list[FooBarEnum])


