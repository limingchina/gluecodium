

from smoke.Alphabet import Alphabet
from smoke.foo.Alphabet import Alphabet
import typing


from _native_base import _NativeBase

import generated


class NameClashLists(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_NameClashLists):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_NameClashLists(*[_unwrap(arg) for arg in args]))


    @property
    def field_a(self) -> list[Alphabet]:
        """"""
        return _wrap(self._native.field_a, list[Alphabet])
    @field_a.setter
    def field_a(self, value: list[Alphabet]):
      self._native.field_a = _unwrap(value, list[Alphabet])



    @property
    def field_b(self) -> list[Alphabet]:
        """"""
        return _wrap(self._native.field_b, list[Alphabet])
    @field_b.setter
    def field_b(self, value: list[Alphabet]):
      self._native.field_b = _unwrap(value, list[Alphabet])


