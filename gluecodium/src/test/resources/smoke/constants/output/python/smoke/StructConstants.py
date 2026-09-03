

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class StructConstants(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructConstants.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructConstants.SomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
        @property
        def float_field(self) -> float:
            return _wrap(self._native.float_field, float)
        @float_field.setter
        def float_field(self, value: float):
          self._native.float_field = _unwrap(value, float)
    
    
    
    
    class NestingStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructConstants.NestingStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructConstants.NestingStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def struct_field(self) -> StructConstants.SomeStruct:
            return _wrap(self._native.struct_field, StructConstants.SomeStruct)
        @struct_field.setter
        def struct_field(self, value: StructConstants.SomeStruct):
          self._native.struct_field = _unwrap(value, StructConstants.SomeStruct)
    
    
    

    STRUCT_CONSTANT = {"bar Buzz", 1.41}

    NESTING_STRUCT_CONSTANT = {{"nonsense", -2.82}}

