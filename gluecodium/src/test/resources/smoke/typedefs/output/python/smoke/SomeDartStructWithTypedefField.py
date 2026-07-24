

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class SomeDartStructWithTypedefField(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SomeDartStructWithTypedefField):
            super().__init__(args[0])
        else:
            super().__init__(generated.SomeDartStructWithTypedefField(*[_unwrap(arg) for arg in args]))


    @property
    def some_field(self) -> list[float]:
        """"""
        return _wrap(self._native.some_field, list[float])
    @some_field.setter
    def some_field(self, value: list[float]):
      self._native.some_field = _unwrap(value, list[float])


