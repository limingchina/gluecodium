

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class OuterStructWithFieldConstructorInnerStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStructWithFieldConstructorInnerStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithFieldConstructorInnerStructWithDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def inner_struct_field(self) -> float:
        """"""
        return _wrap(self._native.inner_struct_field, float)
    @inner_struct_field.setter
    def inner_struct_field(self, value: float):
      self._native.inner_struct_field = _unwrap(value, float)


