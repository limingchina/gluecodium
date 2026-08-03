

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class NestedReferences(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def inside_out(self, struct1: NestedReferences.NestedReferences, struct2: NestedReferences.NestedReferences) -> NestedReferences:
        return _wrap(self._native.inside_out(_unwrap(struct1, NestedReferences.NestedReferences), _unwrap(struct2, NestedReferences.NestedReferences)), NestedReferences)

    class NestedReferences(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NestedReferences.NestedReferences):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_NestedReferences.NestedReferences(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
    

