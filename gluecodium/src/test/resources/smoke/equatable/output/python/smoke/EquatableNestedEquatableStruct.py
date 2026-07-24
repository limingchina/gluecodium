

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class EquatableNestedEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EquatableNestedEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.EquatableNestedEquatableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def foo_field(self) -> str:
        """"""
        return _wrap(self._native.foo_field, str)
    @foo_field.setter
    def foo_field(self, value: str):
      self._native.foo_field = _unwrap(value, str)


