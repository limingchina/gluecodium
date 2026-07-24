

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.Alphabet import Alphabet
from smoke.foo.Alphabet import Alphabet


from _native_base import _NativeBase

import generated


class LearnToRead(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.LearnToRead):
            super().__init__(args[0])
        else:
            super().__init__(generated.LearnToRead(*[_unwrap(arg) for arg in args]))


    @property
    def field_a(self) -> Alphabet:
        """"""
        return _wrap(self._native.field_a, Alphabet)
    @field_a.setter
    def field_a(self, value: Alphabet):
      self._native.field_a = _unwrap(value, Alphabet)



    @property
    def field_b(self) -> Alphabet:
        """"""
        return _wrap(self._native.field_b, Alphabet)
    @field_b.setter
    def field_b(self, value: Alphabet):
      self._native.field_b = _unwrap(value, Alphabet)


