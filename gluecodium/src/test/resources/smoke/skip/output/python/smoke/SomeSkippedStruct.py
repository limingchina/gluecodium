

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.SomeSkippedEnum import SomeSkippedEnum


from _native_base import _NativeBase

import generated


class SomeSkippedStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SomeSkippedStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SomeSkippedStruct(
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
    def field(self) -> list[SomeSkippedEnum]:
        """"""
        return _wrap(self._native.field, list[SomeSkippedEnum])
    @field.setter
    def field(self, value: list[SomeSkippedEnum]):
      self._native.field = _unwrap(value, list[SomeSkippedEnum])


