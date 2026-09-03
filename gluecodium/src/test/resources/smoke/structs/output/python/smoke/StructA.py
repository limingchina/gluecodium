

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class StructA(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructA):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructA(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def field(self) -> list[StructB]:
        return _wrap(self._native.field, list[StructB])
    @field.setter
    def field(self, value: list[StructB]):
      self._native.field = _unwrap(value, list[StructB])



from smoke.StructB import StructB
