

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Alphabet import Alphabet as smoke_Alphabet
from smoke.foo.Alphabet import Alphabet as smoke_foo_Alphabet

class NameClashLists(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NameClashLists):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_NameClashLists(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def field_a(self) -> list[smoke_Alphabet]:
        return _wrap(self._native.field_a, list[smoke_Alphabet])
    @field_a.setter
    def field_a(self, value: list[smoke_Alphabet]):
      self._native.field_a = _unwrap(value, list[smoke_Alphabet])


    @property
    def field_b(self) -> list[smoke_foo_Alphabet]:
        return _wrap(self._native.field_b, list[smoke_foo_Alphabet])
    @field_b.setter
    def field_b(self, value: list[smoke_foo_Alphabet]):
      self._native.field_b = _unwrap(value, list[smoke_foo_Alphabet])



