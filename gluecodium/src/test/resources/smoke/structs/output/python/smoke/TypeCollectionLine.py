

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.TypeCollectionPoint import TypeCollectionPoint


from _native_base import _NativeBase

import generated


class TypeCollectionLine(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeCollectionLine):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeCollectionLine(*[_unwrap(arg) for arg in args]))


    @property
    def a(self) -> TypeCollectionPoint:
        """"""
        return _wrap(self._native.a, TypeCollectionPoint)
    @a.setter
    def a(self, value: TypeCollectionPoint):
      self._native.a = _unwrap(value, TypeCollectionPoint)



    @property
    def b(self) -> TypeCollectionPoint:
        """"""
        return _wrap(self._native.b, TypeCollectionPoint)
    @b.setter
    def b(self, value: TypeCollectionPoint):
      self._native.b = _unwrap(value, TypeCollectionPoint)


