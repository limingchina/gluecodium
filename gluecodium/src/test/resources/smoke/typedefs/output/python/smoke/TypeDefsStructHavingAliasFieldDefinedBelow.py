

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class TypeDefsStructHavingAliasFieldDefinedBelow(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeDefsStructHavingAliasFieldDefinedBelow):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeDefsStructHavingAliasFieldDefinedBelow(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> float:
        """"""
        return _wrap(self._native.field, float)
    @field.setter
    def field(self, value: float):
      self._native.field = _unwrap(value, float)


