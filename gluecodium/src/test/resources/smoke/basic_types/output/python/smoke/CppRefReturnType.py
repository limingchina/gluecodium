

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class CppRefReturnType(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def void_ref():
        generated.smoke_CppRefReturnType.void_ref()

    @staticmethod
    def bool_ref() -> bool:
        return generated.smoke_CppRefReturnType.bool_ref()

    @staticmethod
    def string_ref() -> str:
        return generated.smoke_CppRefReturnType.string_ref()

    @staticmethod
    def struct_ref() -> CppRefReturnType.SomeStruct:
        native_result = generated.smoke_CppRefReturnType.struct_ref()
        return _get_or_create_wrapper(native_result, CppRefReturnType.SomeStruct)

    @staticmethod
    def class_ref() -> CppRefReturnType:
        native_result = generated.smoke_CppRefReturnType.class_ref()
        return _get_or_create_wrapper(native_result, CppRefReturnType)

    @staticmethod
    def nullable_ref() -> Optional[str]:
        return generated.smoke_CppRefReturnType.nullable_ref()

    @staticmethod
    def throwing_enum_with_void():
        generated.smoke_CppRefReturnType.throwing_enum_with_void()

    @staticmethod
    def throwing_enum_with_string() -> str:
        return generated.smoke_CppRefReturnType.throwing_enum_with_string()

    @staticmethod
    def throwing_struct_with_void():
        generated.smoke_CppRefReturnType.throwing_struct_with_void()

    @staticmethod
    def throwing_struct_with_string() -> str:
        return generated.smoke_CppRefReturnType.throwing_struct_with_string()

    @staticmethod
    def string_property() -> str:
        return _wrap(generated.smoke_CppRefReturnType.string_property(), str)

    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CppRefReturnTypeSomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_CppRefReturnTypeSomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def field(self) -> str:
            return _wrap(self._native.field, str)
        @field.setter
        def field(self, value: str):
          self._native.field = _unwrap(value, str)
    
    
    
    
    class InternalError(Enum):
    
        FOO = generated.smoke_CppRefReturnTypeInternalError.FOO
        BAR = generated.smoke_CppRefReturnTypeInternalError.BAR
    
        @property
        def _native(self):
            return self.value
    
    
    
    class EnumBasedError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    class StructBasedError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

