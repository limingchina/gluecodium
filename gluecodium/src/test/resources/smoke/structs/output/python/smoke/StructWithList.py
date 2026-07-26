

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithList(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructWithList):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructWithList(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> list[StructWithList]:
        """"""
        return _wrap(self._native.field, list[StructWithList])
    @field.setter
    def field(self, value: list[StructWithList]):
      self._native.field = _unwrap(value, list[StructWithList])


