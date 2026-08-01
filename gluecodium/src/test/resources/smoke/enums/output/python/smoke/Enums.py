

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Enums(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_enumeration(input: Enums.SimpleEnum) -> Enums.SimpleEnum:
        native_result = generated.smoke_Enums.method_with_enumeration(_unwrap(input, Enums.SimpleEnum))
        return _get_or_create_wrapper(native_result, Enums.SimpleEnum)

    @staticmethod
    def flip_enum_value(input: Enums.InternalErrorCode) -> Enums.InternalErrorCode:
        native_result = generated.smoke_Enums.flip_enum_value(_unwrap(input, Enums.InternalErrorCode))
        return _get_or_create_wrapper(native_result, Enums.InternalErrorCode)

    @staticmethod
    def extract_enum_from_struct(input: Enums.ErrorStruct) -> Enums.InternalErrorCode:
        native_result = generated.smoke_Enums.extract_enum_from_struct(_unwrap(input, Enums.ErrorStruct))
        return _get_or_create_wrapper(native_result, Enums.InternalErrorCode)

    @staticmethod
    def create_struct_with_enum_inside(type: Enums.InternalErrorCode, message: str) -> Enums.ErrorStruct:
        native_result = generated.smoke_Enums.create_struct_with_enum_inside(_unwrap(type, Enums.InternalErrorCode), _unwrap(message, str))
        return _get_or_create_wrapper(native_result, Enums.ErrorStruct)

    class ErrorStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumsErrorStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_EnumsErrorStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def type(self) -> Enums.InternalErrorCode:
            return _wrap(self._native.type, Enums.InternalErrorCode)
        @type.setter
        def type(self, value: Enums.InternalErrorCode):
          self._native.type = _unwrap(value, Enums.InternalErrorCode)
    
    
        @property
        def message(self) -> str:
            return _wrap(self._native.message, str)
        @message.setter
        def message(self, value: str):
          self._native.message = _unwrap(value, str)
    
    
    
    
    class SimpleEnum(Enum):
    
        FIRST = 0
        SECOND = 1
    
    
    
    class InternalErrorCode(Enum):
    
        ERROR_NONE = 0
        ERROR_FATAL = 1
    
    
    
    dict[Enums.SimpleEnum, int] = dict[Enums.SimpleEnum, int]
    
    

