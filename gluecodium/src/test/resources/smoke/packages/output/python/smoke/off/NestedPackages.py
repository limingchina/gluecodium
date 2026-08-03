

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class NestedPackages(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def basic_method(input: NestedPackages.SomeStruct) -> NestedPackages.SomeStruct:
        native_result = generated.smoke_off_NestedPackages.basic_method(_unwrap(input, NestedPackages.SomeStruct))
        return _get_or_create_wrapper(native_result, NestedPackages.SomeStruct)

    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_off_NestedPackages.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_off_NestedPackages.SomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    

