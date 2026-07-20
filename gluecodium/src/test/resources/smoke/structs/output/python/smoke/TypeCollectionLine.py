

from __future__ import annotations

from smoke.TypeCollectionPoint import TypeCollectionPoint


from _native_base import _NativeBase

import generated


class TypeCollectionLine(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeCollectionLine):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeCollectionLine(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def a(self) -> TypeCollectionPoint:
        """"""
        return TypeCollectionPoint(self._native.a)
    @a.setter
    def a(self, value: TypeCollectionPoint):
      self._native.a = getattr(value, "_native", value)



    @property
    def b(self) -> TypeCollectionPoint:
        """"""
        return TypeCollectionPoint(self._native.b)
    @b.setter
    def b(self, value: TypeCollectionPoint):
      self._native.b = getattr(value, "_native", value)


