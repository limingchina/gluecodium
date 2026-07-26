

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.OuterStructWithFieldConstructorInnerStructWithDefaults import OuterStructWithFieldConstructorInnerStructWithDefaults


from _native_base import _NativeBase

import generated


class OuterStructWithFieldConstructor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_OuterStructWithFieldConstructor):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStructWithFieldConstructor(*[_unwrap(arg) for arg in args]))


    @property
    def outer_struct_field(self) -> OuterStructWithFieldConstructorInnerStructWithDefaults:
        """"""
        return _wrap(self._native.outer_struct_field, OuterStructWithFieldConstructorInnerStructWithDefaults)
    @outer_struct_field.setter
    def outer_struct_field(self, value: OuterStructWithFieldConstructorInnerStructWithDefaults):
      self._native.outer_struct_field = _unwrap(value, OuterStructWithFieldConstructorInnerStructWithDefaults)


