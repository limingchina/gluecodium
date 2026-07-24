

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithMap(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructWithMap):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithMap(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> dict[str, StructWithMap]:
        """"""
        return _wrap(self._native.field, dict[str, StructWithMap])
    @field.setter
    def field(self, value: dict[str, StructWithMap]):
      self._native.field = _unwrap(value, dict[str, StructWithMap])


