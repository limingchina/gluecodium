

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class OuterStructWithFieldConstructorInnerStructWithDefaults(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStructWithFieldConstructorInnerStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStructWithFieldConstructorInnerStructWithDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def inner_struct_field(self) -> float:
        return _wrap(self._native.inner_struct_field, float)
    @inner_struct_field.setter
    def inner_struct_field(self, value: float):
      self._native.inner_struct_field = _unwrap(value, float)


