

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.bar.Alphabet import Alphabet as smoke_bar_Alphabet
from smoke.foo.Alphabet import Alphabet as smoke_foo_Alphabet

class LearnToReadAgain(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_LearnToReadAgain):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_LearnToReadAgain(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def field_b(self) -> smoke_foo_Alphabet:
        return _wrap(self._native.field_b, smoke_foo_Alphabet)
    @field_b.setter
    def field_b(self, value: smoke_foo_Alphabet):
      self._native.field_b = _unwrap(value, smoke_foo_Alphabet)


    @property
    def field_c(self) -> smoke_bar_Alphabet:
        return _wrap(self._native.field_c, smoke_bar_Alphabet)
    @field_c.setter
    def field_c(self, value: smoke_bar_Alphabet):
      self._native.field_c = _unwrap(value, smoke_bar_Alphabet)



