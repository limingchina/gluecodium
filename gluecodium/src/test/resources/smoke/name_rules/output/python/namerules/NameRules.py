

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class NameRules(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> NameRules:
        native_result = generated.namerules_NameRules.create()
        return _get_or_create_wrapper(native_result, NameRules)

    def some_method(self, some_argument: NameRules.ExampleStruct) -> float:
        return _wrap(self._native.some_method(_unwrap(some_argument, NameRules.ExampleStruct)), float)

    @property
    def int_property(self) -> int:
        return _wrap(self._native.int_property, int)

    @int_property.setter
    def int_property(self, value: int):
        self._native.int_property = _unwrap(value, int)

    @property
    def is_boolean_property(self) -> bool:
        return _wrap(self._native.is_boolean_property, bool)

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool):
        self._native.is_boolean_property = _unwrap(value, bool)

    @property
    def struct_property(self) -> NameRules.ExampleStruct:
        return _wrap(self._native.struct_property, NameRules.ExampleStruct)

    @struct_property.setter
    def struct_property(self, value: NameRules.ExampleStruct):
        self._native.struct_property = _unwrap(value, NameRules.ExampleStruct)

    class ExampleStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.namerules_NameRules.ExampleStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.namerules_NameRules.ExampleStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def value(self) -> float:
            return _wrap(self._native.value, float)
        @value.setter
        def value(self, value: float):
          self._native.value = _unwrap(value, float)
    
    
        @property
        def int_value(self) -> list[int]:
            return _wrap(self._native.int_value, list[int])
        @int_value.setter
        def int_value(self, value: list[int]):
          self._native.int_value = _unwrap(value, list[int])
    
    
    
    
    class ExampleErrorCode(Enum):
    
        NONE = generated.namerules_NameRules.ExampleErrorCode.NONE
        FATAL = generated.namerules_NameRules.ExampleErrorCode.FATAL
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ExampleError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    StringArray = list[str]
    
    

