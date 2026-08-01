

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class OuterStructWithFieldConstructor(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStructWithFieldConstructor):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStructWithFieldConstructor(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def outer_struct_field(self) -> OuterStructWithFieldConstructor.InnerStructWithDefaults:
        return _wrap(self._native.outer_struct_field, OuterStructWithFieldConstructor.InnerStructWithDefaults)
    @outer_struct_field.setter
    def outer_struct_field(self, value: OuterStructWithFieldConstructor.InnerStructWithDefaults):
      self._native.outer_struct_field = _unwrap(value, OuterStructWithFieldConstructor.InnerStructWithDefaults)


    class InnerStructWithDefaults(_NativeBase):
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
    
    
    

