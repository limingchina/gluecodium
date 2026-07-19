

from __future__ import annotations

from smoke.bar.Alphabet import Alphabet
from smoke.foo.Alphabet import Alphabet


from _native_base import _NativeBase

import generated


class LearnToReadAgain(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.LearnToReadAgain):
            super().__init__(args[0])
        else:
            super().__init__(generated.LearnToReadAgain(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field_b(self) -> Alphabet:
        """"""
        return Alphabet(self._native.field_b)
    @field_b.setter
    def field_b(self, value: Alphabet):
      self._native.field_b = getattr(value, "_native", value)



    @property
    def field_c(self) -> Alphabet:
        """"""
        return Alphabet(self._native.field_c)
    @field_c.setter
    def field_c(self, value: Alphabet):
      self._native.field_c = getattr(value, "_native", value)


