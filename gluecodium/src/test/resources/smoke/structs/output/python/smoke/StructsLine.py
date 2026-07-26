

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructsPoint import StructsPoint


from _native_base import _NativeBase

import generated


class StructsLine(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructsLine):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsLine(*[_unwrap(arg) for arg in args]))


    @property
    def a(self) -> StructsPoint:
        """"""
        return _wrap(self._native.a, StructsPoint)
    @a.setter
    def a(self, value: StructsPoint):
      self._native.a = _unwrap(value, StructsPoint)



    @property
    def b(self) -> StructsPoint:
        """"""
        return _wrap(self._native.b, StructsPoint)
    @b.setter
    def b(self, value: StructsPoint):
      self._native.b = _unwrap(value, StructsPoint)


