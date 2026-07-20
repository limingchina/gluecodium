

from __future__ import annotations

from smoke.StructsPoint import StructsPoint


from _native_base import _NativeBase

import generated


class StructsLine(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsLine):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsLine(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def a(self) -> StructsPoint:
        """"""
        return StructsPoint(self._native.a)
    @a.setter
    def a(self, value: StructsPoint):
      self._native.a = getattr(value, "_native", value)



    @property
    def b(self) -> StructsPoint:
        """"""
        return StructsPoint(self._native.b)
    @b.setter
    def b(self, value: StructsPoint):
      self._native.b = getattr(value, "_native", value)


