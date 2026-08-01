

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class PublicFieldsMixedInit(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicFieldsMixedInit):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicFieldsMixedInit(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def public_field1(self) -> str:
        return _wrap(self._native.public_field1, str)
    @public_field1.setter
    def public_field1(self, value: str):
      self._native.public_field1 = _unwrap(value, str)


    @property
    def public_field2(self) -> str:
        return _wrap(self._native.public_field2, str)
    @public_field2.setter
    def public_field2(self, value: str):
      self._native.public_field2 = _unwrap(value, str)



