

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class EquatableStructWithAccessors(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EquatableStructWithAccessors):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EquatableStructWithAccessors(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._native == other._native

    def __hash__(self) -> int:
        return hash(self._native)

    @property
    def foo_field(self) -> str:
        return _wrap(self._native.foo_field, str)
    @foo_field.setter
    def foo_field(self, value: str):
      self._native.foo_field = _unwrap(value, str)



