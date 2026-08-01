

from enum import Enum
import typing

class Enums:

    @staticmethod
    def method_with_enumeration(input: Enums.SimpleEnum) -> Enums.SimpleEnum:
        ...

    @staticmethod
    def flip_enum_value(input: Enums.InternalErrorCode) -> Enums.InternalErrorCode:
        ...

    @staticmethod
    def extract_enum_from_struct(input: Enums.ErrorStruct) -> Enums.InternalErrorCode:
        ...

    @staticmethod
    def create_struct_with_enum_inside(type: Enums.InternalErrorCode, message: str) -> Enums.ErrorStruct:
        ...

    class ErrorStruct:
    
        type: Enums.InternalErrorCode
    
        message: str
    
    
    
    class SimpleEnum(Enum):
    
        FIRST = 0
        SECOND = 1
    
    
    
    class InternalErrorCode(Enum):
    
        ERROR_NONE = 0
        ERROR_FATAL = 1
    
    
    
    dict[Enums.SimpleEnum, int] = dict[Enums.SimpleEnum, int]
    
    

