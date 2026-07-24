

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithSet(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructWithSet):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithSet(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> set[StructWithSet]:
        """"""
        return _wrap(self._native.field, set[StructWithSet])
    @field.setter
    def field(self, value: set[StructWithSet]):
      self._native.field = _unwrap(value, set[StructWithSet])


